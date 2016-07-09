__author__ = "geduldig"
__date__ = "December 7, 2012"
__license__ = "MIT"

import re

class Tokenizer:
	"""Class methods for parsing tweets into lists of lower case words."""
	
	@classmethod
	def _remove_urls(cls, tweet):
		return re.sub('((www\.[\s]+)|(https?://[^\s]+))', ' ', tweet) 

	@classmethod
	def _remove_html_char_codes(cls, tweet):
		return re.sub('&[a-z]{1,6};', ' ', tweet) 

	@classmethod
	def _remove_non_alphanumerics(cls, tweet):
		# Don't remove '_', '@', '#'
		return re.sub('[\`\~\!\$\%\^\&\*\(\)\-\+\=\[\]\{\}\\\|\;\:\'\"\,\<\.\>\/\?]', ' ', tweet)

	@classmethod
	def _remove_numbers(cls, tweet):
		return re.sub('(\s|^)?[0-9]+(\s|$)?', ' ', tweet) 

	@classmethod
	def _remove_RT(cls, tweet):
		return re.sub('(\s^)?rt(\s$)?', ' ', tweet)

	@classmethod
	def _remove_duplicates(cls, tweet, chars):
		return re.sub('[%s]{2,}' % chars, ' ', tweet) 

	@classmethod
	def _remove_nonlatin_unicode(cls, tweet):
		return re.sub(u'[\u0000-\u001f\u007f-\uffff]', ' ', tweet) 

	@classmethod
	def _remove_short_words(cls, tweet, length):
		return [word for word in tweet.split() if len(word) > length]

	@classmethod
	def hashtags(cls, tweet, only_latin_alphabet=False):
		"""Get hashtags from tweets.  
		
		tweet : Raw tweet text.
			
		Return: list
			hashtags
		"""
		tweet = tweet.lower()
		tweet = cls._remove_html_char_codes(tweet)
		tweet = cls._remove_non_alphanumerics(tweet)
		tweet = cls._remove_duplicates(tweet, '#')
		if only_latin_alphabet:
			tweet = cls._remove_nonlatin_unicode(tweet)
		return re.findall('#\w+', tweet)

	@classmethod
	def plain_text(cls, tweet, min_length=3, only_latin_alphabet=False):
		"""Get words from tweets.  
		
		tweet : Raw tweet text.
			
		Return : list
			Lower case words with at least 3 character, excluding non-latin
			characters and digits not connected to letters.
		"""
		tweet = tweet.lower()
		tweet = cls._remove_urls(tweet)
		tweet = cls._remove_html_char_codes(tweet)
		tweet = cls._remove_non_alphanumerics(tweet)
		tweet = cls._remove_numbers(tweet)
		tweet = cls._remove_RT(tweet)
		tweet = cls._remove_duplicates(tweet, '#@')
		if only_latin_alphabet:
			tweet = cls_remove_nonlatin_unicode(tweet)
		return cls._remove_short_words(tweet, min_length)
	
