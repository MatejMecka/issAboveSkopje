import xml.etree.ElementTree as ET
import urllib.request
import tweepy
import sched, time
import threading
import serial
from time import time, sleep
from random import randrange
from threading import Timer
from datetime import datetime, date, time

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

followers = api.followers_ids(id='issaboveskopje')

# Connect to Arduino (Optional, for lights)
try:
	arduinoData = serial.Serial('/dev/ttyUSB0', 9600)
except Exception as e:
	print(e)

tm = ''
dr = ''
dt = ''
sve = dict()


postArt = """
		The International Space Station is above Skopje!
	           .       .                   .       .      .     .      .
    .       . 	.     .    .            .         ______
      .           .             .               ////////
                .    .   ________   .  .      /////////     .    .
           .            |.____.  /\        ./////////    .
    .                 .//      \/  |\     /////////
       .       .    .//          \ |  \ /////////       .     .   .
                    ||.    .    .| |  ///////// .     .
     .    .         ||           | |//`,/////                .
             .       \	       ./ //  /  \/   .
  .                    \.____./ //\` '   ,_\     .     .
          .           .     \ //////\ , /   \                 .    .
                       .    ///////// \|  '  |    .
      .        .          ///////// .   \ _ /          .
                        /////////                              .
                 .   ./////////     .
         .           --------   .                  ..
  .               .        .         .

             .            ___---___                    .
       .              .--\        --.     .     .         .
                    ./.;_.\     __/~ \.
                   /;  / `-'  __\    . \	.
 .        .       / ,--'     / .   .;   \        |
                 | .|       /       __   |      -O-       .
                |__/    __ |  . ;   \ | . |      |
                |      /  \_     . ;| \___|
   .    o       |      \  .~\_ __,--'     |           .
                 |     | . ; ~~~~\_    __|
    |             \    \   .  .  ; \  /_/   . 	.
   -O-        .    \   /         . |  ~/
    |    .          ~\ \   .      /  /~          o
  .                   ~--___ ; ___--~
                 .          ---         .
			HACKLAB KIKA
"""


# Take the RSS feed once per day, split the lines (date, time, approach etc..) and read them

def oncePerDay():
	# Using local XML for testing purposes
	#tree = ET.parse('Macedonia_None_Skopje.xml')
	#root = tree.getroot()

	fetched = urllib.request.urlopen('http://spotthestation.nasa.gov/sightings/xml_files/Macedonia_None_Skopje.xml')
	tree = ET.parse(fetched)
	root = tree.getroot()

	titles = root.findall('channel/item/title')
	descriptions = root.findall('channel/item/description')

	for item in descriptions:

		lst = item.text.strip().split('\n')

		for line in lst:
			line = line.replace('<br/>', '').strip()
			if line.startswith('Date:'):
				dt = line[6:]
				print('\nДата: ', dt)

			if line.startswith('Time:'):
				tm = line[6:]
				print('Време: ', tm)


			if line.startswith('Duration:'):
				dr = line[10:11]
				print('Времетраење: ', dr, 'мин.')

			if line.startswith('Approach:'):
				ar = line[10:]
				ar = ar.replace('above', 'над')
				ar = ar.replace('N', 'С	')
				ar = ar.replace('S', 'J')
				ar = ar.replace('E', 'И')
				ar = ar.replace('W', 'З')
				if len(ar) == 11:
					ar = ar[:9] + '-' + ar[9:]
				print('Приоѓа од: ', ar)

			if line.startswith('Departure:'):
				dp = line[11:]
				dp = dp.replace('above', 'над')
				dp = dp.replace('N', 'С')
				dp = dp.replace('S', 'J')
				dp = dp.replace('E', 'И')
				dp = dp.replace('W', 'З')
				if len(dp) == 11:
					dp = dp[:9] + '-' + dp[9:]
				print('Заминува кон: ', dp)
				if dt not in sve:
					sve[dt] = []
				sve[dt].append((tm, dr, ar, dp))

	threading.Timer(86400, oncePerDay).start()

# Picks random message to make the tweet

def pick_msg(dur, app, dpr):
	foo = ['Сателитот е над Скопје!',
		'Вселенската Станица го надлетува Скопје во моментов!',
		'Хјустон! Вселенската Станица е над Скопје!']
	random_index = randrange(0,len(foo))

	if dur == 'l':
		dur = 'помалку од 1'

	# Post status on Twitter
	api.update_status(foo[random_index] + ' Времетраeње: ' + dur + ' мин.' + ' Приоѓа од: ' + app + ', заминува кон: ' + dpr)

# Check if someone wants disable DM's
def statusMentions():
	mentions = api.mentions_timeline()
	disabled_set = set()

	for mention in mentions:
		if mention.text == '@ISSAboveSkopje disableDM':
			disabled_set.add(str(mention.user.id))
			
	print(disabled_set)
	print(','.join([str(x) for x in followers]))
	with open('ids.txt', 'w') as w:
		for follower in followers:
			if str(follower) in disabled_set: continue
			w.write(str(follower) + '\n')

	threading.Timer(40, statusMentions).start()

# Send DM to followers.
def pick_dm(dur, app, dpr):
	with open('ids.txt', 'r+') as s:
		lines = s.readlines()
		#print(lines)
	follower_dm = "Сателитот е над Скопје! Излези!" + ' Времетраeње: ' + dur + ' мин.' + ' Приоѓа од: ' + app + ', заминува кон: ' + dpr
	for follower_id in lines:
		print(follower_id)
		api.send_direct_message(user=follower_id, text=follower_dm)

# Check if the datetime.now is the same as the time of the RSS feed, if so, post to twitter
def twitterPost():
	if datetime.now().strftime("%A %b %-d, %Y") in sve:
		for t in sve[datetime.now().strftime("%A %b %-d, %Y")]:
			if datetime.now().strftime("%-I:%M %p") == t[0]:

				print(postArt)
				# Try to post a tweet and send DM
				try:
					pick_dm(t[1], t[2], t[3])
					time.sleep(1)
					pick_msg(t[1], t[2], t[3])
				except Exception as e:
					print(e)
				# Try to light up the lights
				try:
					arduinoData.write(b'1')
				except Exception as e:
					print(e)
			else:
				print('Сеуште ништо.')
				try:
					arduinoData.write(b'1')
				except Exception as e:
					print(e)

# Check the datetime again in 60 secs.
def oncePerMinute():
	twitterPost()
	threading.Timer(60, oncePerMinute).start()

statusMentions()
oncePerMinute()
oncePerDay()
