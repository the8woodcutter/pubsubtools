import re
import json
import logging

class NewsGetter():

	def __init__(self):
		try:
			with shelve.open('news') as db:
				latest = db.get('latest')
				db.close()
		except:
			with shelve.open('news') as db:
				latest = {}
				db['latest'] = latest
				db.close()
		finally:
			db = dict(latest)
		self.db = db
		# this we use in a method later:
		# data = {} # json payload, as file or imported into a dict()
		log = {} # dunno yet

	def get_latest(self):
		# https://hacker-news.firebaseio.com/v0/topstories.json
		# curl?  jsonify?  json.loads?  what?  urllib3?

		# compare time in self.db['topstories']['timestamp'] for eval to now
			# (we would do this also for each of other types of API data too)
		
		# curl or make dict() of the URL's json payload!  make it a python type object!
			# now probably (for that URL anyways) going to have to use a sub function to get child data