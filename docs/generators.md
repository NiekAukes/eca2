# Loading data from a file
Neca provides a way to load timestamped data from a file. This is useful for loading data from a file that is being written to by another program. 

This file should have datapoints seperated by newlines. Each datapoint should be a JSON object with a `created_at` field (timestamp format: `%a %b %d %H:%M:%S %z %Y`). If your data is not in this format, you can write a custom generator function to parse it.

This data can then be generated as events by the `generate_data()` function. this function adds the timestamped data to the context's event queue, and emits an event for each datapoint with the appropriate delay.

```python
from neca.generators import generate_data
# Generate and emit tweets from a data file
generate_data('tweets.txt', time_scale=1000, event_name='new_tweet', limit=100) 
```

this function has the following parameters:
- `data_file` (str): The path to the file containing the tweet data.
- `time_scale` (int, optional): The time scale used to convert timestamps in the file to simulation time. Default is 1000, which means that 1 second in the file corresponds to 1 millisecond in the simulation (1000x speedup)
- `event_name` (str, optional): The name of the event to which the tweets should be emitted. Default is 'tweet'.
- `context` (Context, optional): The context in which to emit the events. If None, events are not emitted.
- `limit` (int, optional): The maximum number of tweets to emit. If None, all tweets from the file are emitted.
- `generator` (Callable[[str], Generator], optional): The generator function used to read and parse data from the file. Default is 'tweet_generator'.
- timestamp_signature (Tuple[str,str], optional): The signature of the timestamp field (name, format) in the data file. Default is ('created_at', '%a %b %d %H:%M:%S %z %Y').

## print_object()
The `print_object()` function is used to print an object in human-readable format to the console. This is useful for debugging. 

```python
from neca.generators import print_object
# Print the tweet object to the console
print_object(tweet)
```