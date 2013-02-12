"""
	REQUIRED: PASTE YOUR TWITTER OAUTH CREDENTIALS INTO puttytat/credentials.txt 
	          OR USE -oauth OPTION TO USE A DIFFERENT FILE CONTAINING THE CREDENTIALS.
	
	Counts tweets containing any word that is passed as a command line argument.  
	Prints current count for each tweet found.
	
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
import puttytat

OAUTH = None


def count_tweets_search(list):
	words = ' OR '.join(list)
	count = 0
	while True:
		tw = puttytat.TwitterRestPager(OAUTH)
		for item in tw.request('search/tweets', {'q': words}):
			if 'text' in item:
				count += 1
				print count
			elif 'message' in item:
				if item['code'] == 131:
					continue # ignore internal server error
				elif item['code'] == 88:
					print>>sys.stderr, 'Suspend search until %s' % search.get_quota()['reset']
				raise Exception('Message from twiter: %s' % item['message'])


def count_tweets_stream(list):
	words = ','.join(list)
	count = 0
	total_skip = 0
	while True:
		tw = puttytat.TwitterStream(OAUTH)
		skip = 0
		try:
			while True:
				for item in tw.request('statuses/filter', {'track': words}):
					if 'text' in item:
						count += 1
						print count + skip + total_skip
					elif 'limit' in item:
						skip = item['limit'].get('track')
						print '\n\n\n*** Skipping %d tweets\n\n\n' % (total_skip + skip)
					elif 'disconnect' in item:
						raise Exception('Disconnect: %s' % item['disconnect'].get('reason'))
		except Exception, e:
			print>>sys.stderr, '*** MUST RECONNECT', e
		total_skip += skip


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Count occurance of word(s).')
	parser.add_argument('-oauth', metavar='FILENAME', type=str, help='read OAuth credentials from file')
	parser.add_argument('-past', action='store_true', help='search historic tweets')
	parser.add_argument('words', metavar='W', type=str, nargs='+', help='word(s) to count the occurance of')
	args = parser.parse_args()	

	OAUTH = puttytat.TwitterOauth.read_file(args.oauth)
	
	try:
		if args.past:
			count_tweets_search(args.words)
		else:
			count_tweets_stream(args.words)
	except KeyboardInterrupt:
		print>>sys.stderr, '\nTerminated by user'
	except Exception, e:
		print>>sys.stderr, '*** STOPPED', e
