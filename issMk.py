import xml.etree.ElementTree as ET
from datetime import datetime, date, time
import urllib.request
import tweepy
from time import time, sleep
import sched, time
from random import randrange
from threading import Timer
import threading
import serial

CONSUMER_KEY = "NcgnL2jtiRYDq1sdtbBedka75"
CONSUMER_SECRET = "d7cZFrQhM9T4X3gHmtdrSCZjbqX2mH2LbFIeUxX1K0xvVmzlJB"
ACCESS_KEY = "701094261509464068-RQpxQ8UsWgIQVGIlHKd6SbCrEsR39sW"
ACCESS_SECRET =  "q0xoe1PHaje7O5Q9AbpX4FCmPjUxK8NrEOKKI2PRmtOni"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

arduinoData = serial.Serial('/dev/ttyUSB0', 9600)

api = tweepy.API(auth)

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

def oncePerWeek():
	# for testing purposes
	tree = ET.parse('Macedonia_None_Skopje.xml')
	root = tree.getroot()

	# fetched = urllib.request.urlopen('http://spotthestation.nasa.gov/sightings/xml_files/Macedonia_None_Skopje.xml')
	# tree = ET.parse(fetched)
	# print(type(tree))
	# root = tree.getroot()

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

	threading.Timer(604800, oncePerWeek).start()

def pick_msg(dur, app, dpr):
	foo = ['Сателитот е над Скопје!',
		'Вселенската Станица го надлетува Скопје во моментов!',
		'Хјустон! Вселенската Станица е над Скопје!']
	random_index = randrange(0,len(foo))
	# post to twitter

	if dur == 'l':
		dur = 'помалку од 1'

	api.update_status(foo[random_index] + ' Времетраeње: ' + dur + ' мин.' + ' Приоѓа од: ' + app + ', заминува кон: ' + dpr)

# pick dm and send it to followers
def pick_dm(dur, app, dpr):

	followers = api.followers_ids(id='issaboveskopje')
	follower_dm = "Сателитот е над Скопје! Излези!" + ' Времетраeње: ' + dur + ' мин.' + ' Приоѓа од: ' + app + ', заминува кон: ' + dpr
	for follower in followers:
		api.send_direct_message(user=follower, text=follower_dm)


def twitterPost():
	if datetime.now().strftime("%A %b %-d, %Y") in sve:
		for t in sve[datetime.now().strftime("%A %b %-d, %Y")]:
			if datetime.now().strftime("%-I:%M %p") == t[0]:

				print(postArt)

				pick_dm(t[1], t[2], t[3])
				time.sleep(1)
				pick_msg(t[1], t[2], t[3])
				arduinoData.write(b'1')
			else:
				print('Сеуште ништо.')
				arduinoData.write(b'0')
		#print (datetime.now().strftime("%A %b %-d, %Y"), sve[datetime.now().strftime("%A %b %-d, %Y")])

# start over in 60 sec
def oncePerMinute():
	twitterPost()
	threading.Timer(60, oncePerMinute).start()

oncePerMinute()
oncePerWeek()
