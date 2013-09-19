__author__ = "Jonas Geduldig"
__date__ = "December 7, 2012"
__license__ = "MIT"

import argparse
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager


def process_tweet(text, count, list):
	text = text.lower()
	for word in list:
		if word in text:
			count[word] += 1
	print(count)


def count_old_words(api, list):
	words = ' OR '.join(list)
	count = dict((word,0) for word in list)
	while True:
		pager = TwitterRestPager(api, 'search/tweets', {'q': words})
		for item in pager.get_iterator():
			if 'text' in item:
				process_tweet(item['text'], count, list)
			elif 'message' in item:
				if item['code'] == 131:
					continue # ignore internal server error
				elif item['code'] == 88:
					print('Suspend search until %s' % search.get_quota()['reset'])
				raise Exception('Message from twiter: %s' % item['message'])


def count_new_words(api, list):
	words = ','.join(list)
	count = dict((word,0) for word in list)
	total_skip = 0
	while True:
		skip = 0
		try:
			r = api.request('statuses/filter', {'track': words})
			while True:
				for item in r.get_iterator():
					if 'text' in item:
						process_tweet(item['text'], count, list)
					elif 'limit' in item:
						skip = item['limit'].get('track')
						print('\n\n\n*** Skipped %d tweets\n\n\n' % (total_skip + skip))
					elif 'disconnect' in item:
						raise Exception('Disconnect: %s' % item['disconnect'].get('reason'))
		except Exception as e:
			print('*** MUST RECONNECT %s\n' % e)
		total_skip += skip


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Count occurances of word(s).')
	parser.add_argument('-oauth', metavar='FILENAME', type=str, help='read OAuth credentials from file')
	parser.add_argument('-past', action='store_true', help='search historic tweets')
	parser.add_argument('words', metavar='W', type=str, nargs='+', help='word(s) to count the occurance of')
	args = parser.parse_args()	

	oauth = TwitterOAuth.read_file(args.oauth)
	api = TwitterAPI(oauth.consumer_key, oauth.consumer_secret, oauth.access_token_key, oauth.access_token_secret)
	
	try:
		if args.past:
			count_old_words(api, args.words)
		else:
			count_new_words(api, args.words)
	except KeyboardInterrupt:
		print('\nTerminated by user\n')
	except Exception as e:
		print('*** STOPPED %s\n' % e)
