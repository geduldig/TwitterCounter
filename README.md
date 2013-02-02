### UNDER DEVELOPMENT ###

_Expected release date is sometime in early February 2013_

---

# TwitterCounter #

*Scripts for counting tweets.*

With this package you can count tweets containing a specified word, you can count the frequency of words, and you can rank the most popular words.

The scripts in this package download tweets from twitter.com.  They take one or more search words as command line arguments.  The scripts also take a flag argument for counting either old tweets or current tweets.  The scripts download old tweets using Twitter's REST API and download new tweets using Twitter's Streaming API.

The Twitter API requires OAuth credentials which you can get by creating an application on dev.twitter.com.  Once you have your OAuth secrets and keys, copy them into twittercounter/credentials.txt.  Alternatively, you may specify as a command line argument a file containing your credentials.  Read on for more info.

Twitter restricts searching old tweets to within roughly the past week.  Twitter also places a bandwidth limit on searching current tweets, but you will notice this only when your search contains highly common words.  When this limit occurs the total number of skipped tweets is printed and the connection is maintained.

### Features ###

_The following modules run as command line scripts and write tweet counts to the console.  By default, these scripts search only currently posted tweets.  To search old tweets include the '-past' flag._

### CountTweets ###

Prints a running total of the number of tweets that contain any of the search words.

### CountWords ###

Prints a running total of the number of tweets that contain any search word.

### RankHashtags ###

Prints the most frequently found hashtags in tweets that contain any of the search words.  By default, displays the 3 most popular hashtags and their counts.  To set a different display number use the '-n' option.

### RankReTweets ###

Prints the most frequent re-tweets that contain any of the search words.  By default, displays the 5 most popular re-tweets and their counts.  To set a different display number use the '-n' option.

### RankWords ###

Prints the most frequently found words in tweets that contain any of the search words.  By default, displays the 3 most popular words (excluding the search words and common words) and their counts.  To set a different display number use the '-n' option.

_These are utility modules._

### Tokenizer ###

Contains one class method for extracting hashtags and one for extracting plain text (no URLs, numbers, words shorter than 3 characters, common words).  The latter takes optional arguments for setting the minimum word length and for excluding non-latin characters.

### Words ###

Lists of common English words to ignore.

# Installation #


1. On a command line, type:

`pip install twittercounter`

2. Either copy your OAuth consumer secret and key and your access token secret and key into twittercounter/credentials.txt, or copy them into another file which you will specify on the command line.  See credentials.txt for the expected file format.

3. Then, run a script type with '-m' option, for example:

`python -m twittercount.RankHashtags zzz'
`python -m twittercount.RankHashtags zzz -oauth ./my_credentials.txt`

# External Dependencies #

This package uses the following external package to download tweets from twitter.com:

* twitterapi

# Contributors #

Jonas Geduldig