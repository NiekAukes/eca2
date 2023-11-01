from datetime import datetime
from typing import Optional, Callable, Generator, Tuple
from neca.events import *
import json

import threading

def tweet_generator(data_file: str) -> Generator[dict, None, None]:
    """
    Generate tweet objects from a data file and yield them.

    This generator function reads tweet data from a specified file, parses each line as a JSON-encoded tweet object,
    and yields the parsed tweet objects one by one.

    Parameters:
    - data_file (str): The path to the file containing the tweet data.

    Yields:
    - dict: A parsed tweet object as a Python dictionary.
    ```
    
    Note:
    - The input file should contain one JSON-encoded tweet object per line.
    """

    for line in open(data_file, 'r', encoding='utf-8'):
        tweet = json.loads(line)
        yield tweet

def generate_data(data_file: str, 
                          time_scale: int = 1000, 
                          event_name: str = 'tweet', 
                          context: Optional[Context] = None, 
                          limit: Optional[int] = None,
                          generator: Callable[[str], Generator] = tweet_generator,
                          timestamp_signature: Tuple[str,str] = ('created_at','%a %b %d %H:%M:%S %z %Y')) -> threading.Thread:
    """
    Generate and emit tweet objects from a data file as events.

    This function reads tweet data from a specified file and emits them as events with optional rate-limiting
    and custom event naming. The tweets are converted into event objects and delivered to the provided context.

    Parameters:
    - data_file (str): The path to the file containing the tweet data.
    - time_scale (int, optional): The time scale used to convert timestamps in the file to simulation time.
      Default is 1000, which means that 1 second in the file corresponds to 1 millisecond in the simulation (1000x speedup)
    - event_name (str, optional): The name of the event to which the tweets should be emitted. Default is 'tweet'.
    - context (Context, optional): The context in which to emit the events. If None, events are not emitted.
    - limit (int, optional): The maximum number of tweets to emit. If None, all tweets from the file are emitted.
    - generator (Callable[[str], Generator], optional): The generator function used to read and parse data from the file.
      Default is 'tweet_generator'.
    - timestamp_signature (Tuple[str,str], optional): The signature of the timestamp field (name, format) in the data file.
      Default is ('created_at','%a %b %d %H:%M:%S %z %Y').

    Note:
    - The generator function should be a Callable that takes the data file as input
      and yields data objects.

    Example usage:
    ```python
    # Generate and emit tweets from a data file
    generate_data('tweets.txt', time_scale=1000, event_name='new_tweet', limit=100)
    ```
    """
    thread = threading.Thread(target=__generate_data, args=(data_file, time_scale, event_name, context, limit, generator, timestamp_signature))
    thread.start()
    return thread

def __generate_data(data_file: str, 
                          time_scale: int = 1000, 
                          event_name: str = 'tweet', 
                          context: Optional[Context] = None, 
                          limit: Optional[int] = None,
                          generator: Callable[[str], Generator] = tweet_generator,
                          timestamp_signature: Tuple[str,str] = ('created_at','%a %b %d %H:%M:%S %z %Y')) -> None:
    
    begin_time = None
    begin_actual_time = datetime.now()
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
        tweet_time = datetime.strptime(tweet[timestamp_signature[0]], timestamp_signature[1])
                    #datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
        
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
        
        real_delay = delay - (datetime.now() - begin_actual_time).total_seconds()
        
        # cap the wait time to prevent it taking too long
        # cap at 2 hours at timescale 1
        if real_delay > 2 * 60 * 60 / time_scale:
            real_delay = ((last_time - begin_time).total_seconds() + 2 * 60 * 60) / time_scale
            
        last_time = tweet_time

        
        context.fire(event_name, tweet, real_delay)
            
            
def print_tweet(tweet):
    print_object(tweet)
        

def print_object(object, tab_level=0):
    """
    Print a Python object in a structured and human-readable format.

    This function converts the input object into a dictionary and prints its keys and values in a well-formatted way.
    If a value is itself a dictionary or a list, it will be printed recursively to maintain a structured display.

    Parameters:
    - object: The Python object to be printed.
    - tab_level (int, optional): The initial tabulation level for indentation. Default is 0.

    Example usage:
    ```python
    my_dict = {'name': 'John', 'age': 30, 'address': {'city': 'New York', 'zip': '10001'}}
    print_object(my_dict)
    ```

    Output:
    ```
    name: John
    age: 30
    address:
        city: New York
        zip: 10001
    ```

    Note:
    - This function is useful for debugging and displaying the contents of complex objects in a more readable manner.
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
    