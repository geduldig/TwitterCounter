[![Downloads](https://img.shields.io/pypi/dm/TwitterCounter.svg)](https://crate.io/packages/TwitterCounter)
[![Downloads](https://img.shields.io/pypi/v/TwitterCounter.svg)](https://crate.io/packages/TwitterCounter)

TwitterCounter
==============
Scripts for counting tweets.  Uses 'search/tweets' or 'statuses/filter' Twitter resource to get old or new tweets, respectively.

CountTweets.py
--------------
Counts the number of tweets that contain any word passed on the command line.

Example:

	> python -u -m TwitterCounter.CountTweets red blue

CountWords.py
-------------
Prints a tally count of the occurrence of any word passed on the command line.

Example:

	> python -u -m TwitterCounter.CountWords red blue

RankHashtags.py
---------------
Prints a tally count of the hashtags that appear most frequently in tweets that contain any word passed on the command line.

Example:

	> python -u -m TwitterCounter.RankHashtags red blue

RankReTweets.py
---------------
Prints a tally count of the most re-tweeted tweets that contain any word passed on the command line, and prints the re-tweet text.

Example:

	> python -u -m TwitterCounter.RankRetweets red blue

RankWords.py
------------
Prints a tally count of the words that appear most frequently in tweets that contain any word passed on the command line.

Example:

	> python -u -m TwitterCounter.RankWords red blue
	
Authentication
--------------
See TwitterAPI documentation.

Dependencies
-----------
* TwitterAPI
