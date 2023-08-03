from datetime import datetime
from typing import Optional, Callable, Generator
from neca.events import *
import json

def tweet_generator(data_file: str):
    """
    simple generator that reads tweets from a file and yields them
    :param data_file: the file containing the tweets
    
    """
    for line in open(data_file, 'r'):
        tweet = json.loads(line)
        yield tweet

def generate_offline_tweets(data_file: str, 
                          time_scale: int = 1000, 
                          event_name: str = 'tweet', 
                          context: Optional[Context] = None, 
                          limit: Optional[int] = None,
                          generator: Callable[[str], Generator] = tweet_generator):
    """
    Starts a generator that reads tweets from a file and emits them as events.
    :param event_name: the name of the event to emit
    :param data_file: the file containing the tweets
    :param time_scale: the time scale used to convert the timestamps in the file to simulation time
    :param context: the context to emit the events to
    :param limit: the maximum number of tweets to emit
    :param generator: the generator to use to read the tweets
    """
    
    begin_time = None
    last_time = datetime.now()
    
    if context is None:
        context = Manager.global_context
        
    gen = generator(data_file)
    
    for tweet in gen:
        if limit is not None and limit <= 0:
            break
        if limit is not None:
            limit -= 1
        
        
        # get the time of the tweet
        tweet_time = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        
        # wait until the tweet should be emitted
        # based on the last tweet time and the time scale
        if begin_time is None:
            # first tweet, emit immediately
            begin_time = tweet_time
            last_time = tweet_time
            context.fire(event_name, tweet, 0)
            continue
            
            
        # wait until the tweet should be emitted
        wait = tweet_time - begin_time
        delay = wait.total_seconds() / time_scale
        
        real_delay = (tweet_time - last_time).total_seconds() / time_scale
        
        # cap the wait time to prevent it taking too long
        # cap at 2 hours at timescale 1
        if real_delay > 2 * 60 * 60 / time_scale:
            delay = ((last_time - begin_time).total_seconds() + 2 * 60 * 60) / time_scale
            
        last_time = tweet_time
        
        context.fire(event_name, tweet, delay)
            
            
def print_tweet(tweet):
    print_object(tweet)
        

def print_object(object, tab_level=0):
    """
    prints objects in a more readable format
    """
    # it does this by converting the object to a dict
    # and then printing all keys and values
    # if the value is a dict or list, it is printed recursively
    
    TAB_STRING = " " * 2
    
    # if the object is a dict, print it nicely
    if isinstance(object, dict):
        for key, value in object.items():
            print(TAB_STRING * tab_level, key, ': ', sep='', end='')
            if isinstance(value, dict) or isinstance(value, list):
                print()
                print_object(value, tab_level + 1)
            else:
                print(value)
    
    # if the object is a list, print it nicely
    elif isinstance(object, list):
        for item in object:
            print(TAB_STRING * tab_level, end='')
            if isinstance(item, dict) or isinstance(item, list):
                print()
                print_object(item, tab_level + 1)
            else:
                print(item)
                
    # if the object is neither a dict nor a list, just print it
    else:
        print(object)
    