#
"""
Compute Term Frequency

Input parameters:
tweets.json - json format of tweets acquired via Twitter API

Usage:
python frequency.py tweets.json

Sample output:
Temp: 2.03163251831e-05
"""
#

import sys
import json
from collections import Counter

def main():
    """
    Calculate Term Frequency for each term in all tweets
    """
    with open(sys.argv[1]) as tweet_file:
        # extract 'text' field from tweet object
        _all = (json.loads(line).get('text', '').split() for line in tweet_file)
        # count word frequencies
        frequencies = Counter(word for tweet in _all for word in tweet)

    total = sum(frequencies.values())
    # calculate Tf
    for i ,x in frequencies.iteritems(): print i ,float(x ) /total

if __name__ == '__main__':
    main()