"""
	REQUIRED: PASTE YOUR TWITTER OAUTH CREDENTIALS INTO twittercounter/credentials.txt 
	          OR USE -oauth OPTION TO USE A DIFFERENT FILE CONTAINING THE CREDENTIALS.
	
	Prints the most frequent re-tweets that contain any of the words that are passed 
	as arguments on the command line.  Prints the re-tweeted text along with the count 
	reported by Twitter.  
	
	Set the number of re-tweets with the '-n' option.  The default is the 5 most 
	frequent re-tweets.
	
	By default only real-time tweets are downloaded (using Twitter's Streaming API).  
	To search old tweets (using Twitter's REST API) use the '-past' flag.  Twitter 
	will permit about a week's worth of old tweets to be counted before breaking the 
	connection.
"""

__author__ = "Jonas Geduldig"
__date__ = "December 7, 2012"
__license__ = "MIT"

# unicode printing for Windows 
import sys, codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)

import argparse
import os
import sys
import twitterapi

OAUTH = None

def process_tweet(retweets, item, n):
	text = item['retweeted_status'].get('text')
	count = item['retweet_count']
	inserted = False
	for i in reversed(range(0, len(retweets))):
		if not inserted and count >= retweets[i][0]:
			retweets.insert(i+1, (count, text))
			inserted = True
		if retweets[i][1] == text:
			if inserted:
				del retweets[i]
			else:
				break
	if not inserted and len(retweets) < n:
		retweets.insert(0, (count, text))
		inserted = True
	elif len(retweets) > n:
		del retweets[0]
	if inserted:
		for rt in retweets:
			print '%d: %s' % (rt[0], rt[1])
		print

def rank_retweets_search(list, n):
	words = ' OR '.join(list)
	retweets = []
	search = twitterapi.TwSearch(OAUTH, { 'q': words })
	while True:
		for item in search.past_results():
			if 'retweeted_status' in item:
				process_tweet(retweets, item, n)
			elif 'message' in item:
				if item['code'] == 131:
					continue # ignore internal server error
				elif item['code'] == 88:
					print>>sys.stderr, 'Suspend search until %s' % search.get_quota()['reset']
				raise Exception('Message from twiter: %s' % item['message'])

def rank_retweets_stream(list, n):
	words = ','.join(list)
	retweets = []
	while True:
		try:
			stream = twitterapi.TwStream(OAUTH, { 'track': words })
			while True:
				for item in stream.results():
					if 'retweeted_status' in item:
						process_tweet(retweets, item, n)
					elif 'disconnect' in item:
						raise Exception('Disconnect: %s' % item['disconnect'].get('reason'))
		except Exception, e:
			print>>sys.stderr, '*** MUST RECONNECT', e

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Rank retweets.')
	parser.add_argument('-oauth', metavar='FILENAME', type=str, help='read OAuth credentials from file')
	parser.add_argument('-past', action='store_true', help='search historic tweets')
	parser.add_argument('-n', metavar='N', type=int, default=5, help='number of most popular retweets displayed')
	parser.add_argument('words', metavar='W', type=str, nargs='+', help='word(s) to track')
	args = parser.parse_args()	

	if args.oauth:
		OAUTH = twitterapi.TwCredentials.read_file(args.oauth)
	else:
		path = os.path.dirname(__file__)
		path = os.path.join(path, 'credentials.txt')
		OAUTH = twitterapi.TwCredentials.read_file(path)
	
	try:
		if args.past:
			rank_retweets_search(args.words, args.n)
		else:
			rank_retweets_stream(args.words, args.n)
	except KeyboardInterrupt:
		print>>sys.stderr, '\nTerminated by user'
	except Exception, e:
		print>>sys.stderr, '*** STOPPED', e
