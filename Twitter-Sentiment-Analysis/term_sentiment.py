#
"""
Derive the sentiment of new terms

Input parameters:
AFINN-111.txt  - word and sentiment score
tweets.json - json format of tweets acquired via Twitter API

Usage:
python term_sentiment.py AFINN-111.txt tweets.json

Sample output:
granny -0.333333333333
made 0.845260620117
record 0.0
"""
#

import sys
import json
import string
import unicodedata

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

def main():
    """
    read AFINN classified mood file and tweet dumps,
    classify tweet sentiments and produce new output.
    """
    afinnfile = open(sys.argv[1]) #AFINN first
    tweet_file = open(sys.argv[2]) #tweet dump second arg

    scores = {} # initialize an empty dictionary
    for line in afinnfile:
      term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
      scores[term] = int(score)  # Convert the score to an integer.

    table = string.maketrans("","")
    final = []
    c = 0
    unlisted_scores = {}
    for line in tweet_file:
        c+=1
        tweet = json.loads(line.strip())
        try:
            # get rid of other words than english. Normalize possible ones.
            sentence = unicodedata.normalize('NFKD', tweet['text']).encode('ascii','ignore')
            # remove punctuations and numerals since they don't carry sentiments.
            words = ' '.join(sentence.translate(table, string.punctuation).translate(table, '0123456789').split()).split()
            # produce list of listed (scored) and unlisted (non-sentiment) words
            filtered_listed = list(set([x.lower() for x in words]) & set(scores.keys()))
            filtered_unlisted = list(set([x.lower() for x in words if len(x) >= 3]) - set(scores.keys()) - set(stopwords))
            # score terms which are listed.
            sentiment = sum([scores[x] for x in filtered_listed])
            if filtered_unlisted:
                    for x in filtered_unlisted:
                        try:
                            # determine the sentiments of unscored terms. Basic distribution.
                            unlisted_scores[x] += float(sentiment)/len(filtered_listed)
                            unlisted_scores[x] /= 2
                        except:
                            unlisted_scores[x] = float(sentiment)/len(filtered_listed)

        except:
            continue

    for i,x in unlisted_scores.iteritems(): print i,x

if __name__ == '__main__':
    main()
