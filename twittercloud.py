#!/usr/bin/python

# For any queries please contact at rai5@illinois.edu
# Adapted from Mining the Social Web 2nd Edition by Mathew A. Russell

from __future__ import print_function
import re
import twitter
import pandas as pd
import os
import pickle
from pytagcloud import create_tag_image, make_tags

def search_twitter(twitter_api, q, search_size = 100, stop_count = 1000):
    '''
Modified from Example 1-5 in Mining the Social Web 2nd Edition.
Returns statuses, a list of dictionaries of twitter metadata.

Parameters:
twitter_api: Use twitter.Twitter to create twitter.api.Twitter object.
q (str): search query (e.g. #informatics)
search_size: default 100.
stop_count: stops search when the total size of tweets exceeds stop_count.
'''
    # See https://dev.twitter.com/docs/api/1.1/get/search/tweets
    search_results = twitter_api.search.tweets(q = q, count = search_size)
    statuses = search_results['statuses']

    # Iterate through results by following the cursor until we hit the count number
    while stop_count > len(statuses):
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break

        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
        
        next_results = twitter_api.search.tweets(**kwargs)
        statuses += next_results['statuses']
        print(len(statuses), 'tweets fetched...')
        
    return statuses

def clean_statuses(statuses):
    '''


Parameters:
statuses: a list of dictionaries of tweet metadata returned from
search_twitter() function.
'''
    status_texts = [status['text'] for status in statuses]
    status_texts = [text.encode('ascii', 'ignore') for text in status_texts]

    clean_tweets = []

    
    string_list = []    
    
    # seperate every string into words and add to the list string_list
    for item in status_texts: 
        string_list += str(item).split()
    
    # checks for non-alphabetical (covers @ and #) and also 'http'
    r = re.compile('[^a-zA-Z]|http')
    
    # replace string with empty string if necessary and append to clean_tweets
    for item in string_list: # go through each string in the list 
        if re.match(r, str(item)): # if matches, replace with empty string here
            item = ''
        clean_tweets.append(item) # append the string to the list
    
    clean_tweets = filter(None,clean_tweets) # delete empty strings
    clean_tweets = [x.lower() for x in clean_tweets] # convert all strings to lowercase

    return clean_tweets

def get_counts(words):
    '''
Takes a list of strings and returns a dictionary of {string: frequency}.

Parameters:
words: a list of strings

Examples:
>>> get_counts(['a', 'a', 'b', 'b', 'b', 'c'])
[('b', 3), ('a', 2), ('c', 1)]
'''
    series = pd.Series(words) # create pandas series object
    counts = series.value_counts() # get the frequency count for each tag
    counts = [item for item in counts.iteritems()] # convert to a tuple of form [('a',3),('b',2)]

    return counts


def main():
    
<<<<<<< HEAD
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''
=======
    # https://dev.twitter.com/docs/auth/oauth for more information 
    # on Twitter's OAuth implementation.
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    OAUTH_TOKEN = ''
    OAUTH_TOKEN_SECRET = ''
>>>>>>> ceb04ed3e04a83316811cb2484220dd7b5657bd6

    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)

    twitter_api = twitter.Twitter(auth = auth)

    # Search query, try your own.
    q = '#green infrastructure'

    # calling search_twitter too often will lock you out for 1 hour.
    # we will call search twitter once and save the result in a file.
    if not os.path.isfile('{0}.p'.format(q)):
        results = search_twitter(twitter_api, q)
        pickle.dump(results, open('{0}.p'.format(q), 'wb'))

    # load saved pickle file
    results = pickle.load(open('{0}.p'.format(q), 'rb'))
    # clean the tweets and extract the words we want
    clean_tweets = clean_statuses(results)
    f = open('tweet.txt','w')
    for item in pd.Series(clean_tweets):
        f.write(item)
    f.close()
    # calculate the frequency of each word
    word_count = get_counts(clean_tweets)

    # use PyTagCloud to create a tag cloud
    tags = make_tags(word_count, maxsize = 120)
    # the image is store in 'cloud.png'
    create_tag_image(tags, 'cloud.png', size = (900, 600), fontname = 'Lobster')
    
if __name__ == '__main__':

    main()
