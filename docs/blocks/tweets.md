# Tweets block
## Description
This block is used to display a list of tweets. It can display a tweet based on a tweet object given by the emit function. 

## Requirements
This block requires the following libraries:
- tweets.js
- tweet.css (you may change the contents of this file)

```html
<script src="/static/lib/tweets.js"></script>
<link rel="stylesheet" href="/static/style/tweet.css">
```

## Configuration
```js
{
    max_tweets: n,
}
```

- `max_tweets`: the maximum number of tweets to display

## Actions
the tweets block takes a tweet object or a list of tweet objects as input, and displays the tweet(s) in the browser. The tweet object has the following format:
```js
{
    "id": 1234567890, // tweet id
    "text": "some text", // tweet text
    "user": {
        "name": "some name", // user name
        "screen_name": "some screen name", // user screen name
        "profile_image_url": "some image url", // user profile image url
    },
    "entities": {
        "media": [
            {
                "media_url": "some media url", // media url
            },
            ...
        ]
    }
}
```

## Example
This example is also available as a demo
```html
<div id="tweets"></div>
<script>
    var tweets = tweets_block('tweets');
    connect_block(tweets, 'tweet_stream');
</script>
```

```python
@event("tweet")
def tweet_event(ctx, tweet):
    emit("tweet_stream", tweet)
```