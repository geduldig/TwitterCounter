__author__ = "geduldig"
__date__ = "December 7, 2012"
__license__ = "MIT"

import argparse
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager


COUNT = 100 # search download batch size


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
			print('%d: %s' % (rt[0], rt[1]))
		print


def rank_old_retweets(api, word_list, n):
	words = ' OR '.join(word_list)
	retweets = []
	while True:
		pager = TwitterRestPager(api, 'search/tweets', {'q':words, 'count':COUNT})
		for item in pager.get_iterator():
			if 'retweeted_status' in item:
				process_tweet(retweets, item, n)
			elif 'message' in item:
				if item['code'] == 131:
					continue # ignore internal server error
				elif item['code'] == 88:
					print('Suspend search until %s' % search.get_quota()['reset'])
				raise Exception('Message from twitter: %s' % item['message'])


def rank_new_retweets(api, word_list, n):
	words = ','.join(word_list)
	retweets = []
	while True:
		try:
			r = api.request('statuses/filter', {'track':words})
			while True:
				for item in r.get_iterator():
					if 'retweeted_status' in item:
						process_tweet(retweets, item, n)
					elif 'disconnect' in item:
						raise Exception('Disconnect: %s' % item['disconnect'].get('reason'))
		except Exception as e:
			print('*** MUST RECONNECT %s\n' % e)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Rank retweets.')
	parser.add_argument('-n', metavar='N', type=int, default=5, help='number of most popular retweets displayed')
	parser.add_argument('-oauth', metavar='FILENAME', type=str, help='read OAuth credentials from file')
	parser.add_argument('-past', action='store_true', help='search historic tweets')
	parser.add_argument('words', metavar='W', type=str, nargs='+', help='word(s) to track')
	args = parser.parse_args()	

	oauth = TwitterOAuth.read_file(args.oauth)
	api = TwitterAPI(oauth.consumer_key, oauth.consumer_secret, oauth.access_token_key, oauth.access_token_secret)
	
	try:
		if args.past:
			rank_old_retweets(api, args.words, args.n)
		else:
			rank_new_retweets(api, args.words, args.n)
	except KeyboardInterrupt:
		print('\nTerminated by user\n')
	except Exception as e:
		print('*** STOPPED %s\n' % e)
