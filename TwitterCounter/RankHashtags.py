__author__ = "geduldig"
__date__ = "December 7, 2012"
__license__ = "MIT"

import argparse
import operator
from .Tokenizer import Tokenizer
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager


COUNT = 100 # search download batch size


def process_tweet(text, count, n):
	tokens = Tokenizer.hashtags(text)
	for tok in tokens:
		if tok in count:
			count[tok] += 1
		else:
			count[tok] = 1
	count_list = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
	if len(count_list) > 0:
		print(' '.join('%s-%s' % i for i in count_list[:n]))


def rank_old_hashtags(api, word_list, n):
	words = ' OR '.join(word_list)
	count = {}
	while True:
		pager = TwitterRestPager(api, 'search/tweets', {'q':words, 'count':COUNT})
		for item in pager.get_iterator():
			if 'text' in item:
				process_tweet(item['text'], count, n)
			elif 'message' in item:
				if item['code'] == 131:
					continue # ignore internal server error
				elif item['code'] == 88:
					print('Suspend search until %s' % search.get_quota()['reset'])
				raise Exception('Message from twitter: %s' % item['message'])


def rank_new_hashtags(api, word_list, n):
	words = ','.join(word_list)
	count = {}
	while True:
		try:
			r = api.request('statuses/filter', {'track':words})
			while True:
				for item in r.get_iterator():
					if 'text' in item:
						process_tweet(item['text'], count, n)
					elif 'disconnect' in item:
						raise Exception('Disconnect: %s' % item['disconnect'].get('reason'))
		except Exception as e:
			print('*** MUST RECONNECT %s\n' % e)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Hashtag ranker.')
	parser.add_argument('-n', metavar='N', type=int, default=3, help='number of most frequest words displayed')
	parser.add_argument('-oauth', metavar='FILENAME', type=str, help='read OAuth credentials from file')
	parser.add_argument('-past', action='store_true', help='search historic tweets')
	parser.add_argument('words', metavar='W', type=str, nargs='+', help='word(s) to track')
	args = parser.parse_args()	

	oauth = TwitterOAuth.read_file(args.oauth)
	api = TwitterAPI(oauth.consumer_key, oauth.consumer_secret, oauth.access_token_key, oauth.access_token_secret)
	
	try:
		if args.past:
			rank_old_hashtags(api, args.words, args.n)
		else:
			rank_new_hashtags(api, args.words, args.n)
	except KeyboardInterrupt:
		print('\nTerminated by user\n')
	except Exception as e:
		print('*** STOPPED %s\n' % e)
