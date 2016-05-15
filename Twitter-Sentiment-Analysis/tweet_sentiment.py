#
"""
Derive the sentiment of each tweet

Input parameters:
AFINN-111.txt  - word and sentiment score
tweets.json - json format of tweets acquired via Twitter API

Usage:
python tweet_sentiment.py AFINN-111.txt tweets.json

Sample output:
-3
-5
-2
0
2
4
"""
#
import sys
import json
import string
import unicodedata

def main():
    """
    read AFINN classified mood file and tweet dumps,
    classify tweet sentiments and produce new output.
    """
    afinnfile = open(sys.argv[1]) #AFINN first
    tweet_file = open(sys.argv[2]) #tweet second

    scores = {} # initialize an empty dictionary
    for line in afinnfile:
      term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
      scores[term] = int(score)  # Convert the score to an integer.

    table = string.maketrans("","") # initialize empty table
    final = []
    for line in tweet_file:
        tweet = json.loads(line.strip())
        try:
            sentence = unicodedata.normalize('NFKD', tweet['text']).encode('ascii','ignore')
            words = ' '.join(sentence.translate(table, string.punctuation).split()).split()
            filtered = list(set(scores.keys()) & set([x.lower() for x in words]))
            sentiment = sum([scores[x] for x in filtered])
            print sentiment
        except:
            print 0

if __name__ == '__main__':
    main()
