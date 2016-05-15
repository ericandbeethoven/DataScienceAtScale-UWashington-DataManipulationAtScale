#
"""
Which State is happiest?

Input parameters:
AFINN-111.txt  - word and sentiment score
tweets.json - json format of tweets acquired via Twitter API

Usage:
python happiest_state.py AFINN-111.txt tweets.json

Sample output:
FL
"""
#

import sys
import json
import string
import unicodedata
from operator import itemgetter

TABLE = string.maketrans("", "")  # step 1 of removing punctuations

states = {'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'FL': 'Florida', 'WY': 'Wyoming',
          'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NA': 'National', 'NC': 'North Carolina',
          'ND': 'North Dakota', 'NE': 'Nebraska', 'NY': 'New York', 'RI': 'Rhode Island', 'NV': 'Nevada', 'GU': 'Guam',
          'CO': 'Colorado', 'CA': 'California', 'GA': 'Georgia', 'CT': 'Connecticut', 'OK': 'Oklahoma', 'OH': 'Ohio',
          'KS': 'Kansas', 'SC': 'South Carolina', 'KY': 'Kentucky', 'OR': 'Oregon', 'SD': 'South Dakota',
          'DE': 'Delaware', 'DC': 'District of Columbia', 'HI': 'Hawaii', 'PR': 'Puerto Rico', 'TX': 'Texas',
          'LA': 'Louisiana', 'TN': 'Tennessee', 'PA': 'Pennsylvania', 'VA': 'Virginia', 'VI': 'Virgin Islands',
          'AK': 'Alaska', 'AL': 'Alabama', 'AS': 'American Samoa', 'AR': 'Arkansas', 'VT': 'Vermont', 'IL': 'Illinois',
          'IN': 'Indiana', 'IA': 'Iowa', 'AZ': 'Arizona', 'ID': 'Idaho', 'ME': 'Maine', 'MD': 'Maryland',
          'MA': 'Massachusetts', 'UT': 'Utah', 'MO': 'Missouri', 'MN': 'Minnesota', 'MI': 'Michigan', 'MT': 'Montana',
          'MP': 'Northern Mariana Islands', 'MS': 'Mississippi'}


def extract_info(tweet):
    """
    parse and extract only useful elements from the tweet.
    """
    try:
        sentence = unicodedata.normalize('NFKD', tweet['text']) \
            .encode('ascii', 'ignore')
        words = ' '.join(sentence.translate(TABLE, string.punctuation).split()) \
            .split()
        return {
            'country': tweet['place']['country'],
            'location': tweet['coordinates'],
            'code': tweet['place']['country_code'],
            'state': tweet['place']['full_name'].split(", "),
            'text': words
        }
    except (KeyError, TypeError, IndexError):
        return None


def filter_tweets(tweet_file):
    tweets = [extract_info(json.loads(line)) for line in tweet_file]
    return tweets


def extract_sentiments(afinnfile, parsed_tweets):
    """
    read AFINN sentiment file and tweets from API,
    classify tweet sentiments and produce new output.
    """
    scores = {}  # initialize an empty dictionary
    for line in afinnfile:
        term, score = line.split("\t")
        scores[term] = int(score)
    for temp in parsed_tweets:
        try:
            filtered = list(set(scores.keys()) & \
                            set([x.lower() for x in temp['text']])
                            )
            temp['score'] = sum([scores[x] for x in filtered])
            temp.pop('text')
        except:
            pass
    return parsed_tweets


def main():
    """
    Return the state code of the happiest US state
    """
    # extract necessary data from tweet objects
    extracted = filter_tweets(open(sys.argv[2]))
    # execute sentiment analyzer on the tweet objects; add scores
    scored_tweets = extract_sentiments(open(sys.argv[1]), extracted)
    # sort tweets according the scores and filter US based tweets only.
    tweets_US = sorted(
        [x for x in filter(None, scored_tweets) if x['code'] == 'US'],
        key=itemgetter('score')  # , reverse = True
    )

    # determine the state code through geocoded data.
    try:
        if tweets_US[-1]['state'][1] in states.keys():
            print tweets_US[-1]['state'][1]
        else:
            print (key for key, value in states.items() if value == tweets_US[-1]['state'][0]).next()
    except:
        print "unable to determine location"

if __name__ == '__main__':
    main()
