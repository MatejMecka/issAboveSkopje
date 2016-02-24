import xml.etree.ElementTree as ET
from datetime import datetime, date, time
import urllib.request
import tweepy
from time import time, sleep
import sched, time
from random import randrange
from threading import Timer
import threading


CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_KEY = ""
ACCESS_SECRET = ""



auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

tm = ''
dt = ''
sve = dict()

def oncePerWeek():
	# for testing purposes
	tree = ET.parse('Macedonia_None_Skopje.xml')
	root = tree.getroot()
	#
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
				print(dt)

			if line.startswith('Time:'):
				tm = line[6:]
				print(tm)

				if dt not in sve:
					sve[dt] = []
				sve[dt].append(tm)

			if line.startswith('Duration:'):
				dr = line[10:]
				print(dr)

	threading.Timer(604800, oncePerWeek).start()

def pick_msg():
	foo = ['Сателитот е над Скопје!',
		'Вселенската Станица го надлетува Скопје во моментов!',
		'Хјустон! Вселенската Станица е над Скопје!']
	random_index = randrange(0,len(foo))
	# post to twitter
	api.update_status(foo[random_index] + ' Дата: ' + datetime.now().strftime("%A %b %-d, %Y, %-I:%M %p"))

def twitterPost():
	if datetime.now().strftime("%A %b %-d, %Y") in sve:
		for t in sve[datetime.now().strftime("%A %b %-d, %Y")]:
			if datetime.now().strftime("%-I:%M %p") == t:
				print('++++++++++++++++++++++++++++++++++++')
				print('---------POSTING TO TWITTER---------')
				print('++++++++++++++++++++++++++++++++++++')
				# post to twitter func
				pick_msg()
			else:
				print('------------------------------------')
				print('-----------STILL NOTHING------------')
				print('------------------------------------')

		print (datetime.now().strftime("%A %b %-d, %Y"), sve[datetime.now().strftime("%A %b %-d, %Y")])

# start over in 60 sec
def oncePerMinute():
	twitterPost()
	threading.Timer(60, oncePerMinute).start()

oncePerMinute()
oncePerWeek()
