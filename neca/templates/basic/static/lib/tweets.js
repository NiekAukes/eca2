function tweets(id, config = {
    "tweetLimit": 10,
}) {

    // initialize the block
    var element = document.getElementById(id);
    
    function buildUser(tweet) {
        // create the wrapper
        var wrap = document.createElement("div");
        wrap.className = "tweet-user";

        // add the image
        var img = document.createElement("img");
        img.className = "tweet-user-img";
        img.src = "/static/res/DefaultTwitterUser.png"
        wrap.appendChild(img);

        // add the name
        var name = document.createElement("p");
        name.className = "tweet-user-name";
        name.innerHTML = tweet.user.name;
        wrap.appendChild(name);

        // add the screen name / handle / username
        var screenName = document.createElement("a");
        screenName.className = "tweet-user-screen-name";
        screenName.innerHTML = "@" + tweet.user.screen_name;
        screenName.href = "https://twitter.com/" + tweet.user.screen_name;
        wrap.appendChild(screenName);

        return wrap;
    }

    function buildText(tweet) {
        var text = document.createElement("p");
        text.className = "tweet-text";
        text.innerHTML = tweet.text;

        // use the intities to build links
        var entities = tweet.entities;

        // replace the user mentions
        for (let i = 0; i < entities.user_mentions.length; i++) {
            let mention = entities.user_mentions[i];
            let link = document.createElement("a");
            link.href = "https://twitter.com/" + mention.screen_name;
            link.innerHTML = "@" + mention.screen_name;

            text.innerHTML = text.innerHTML.replace("@" + mention.screen_name, link.outerHTML);
            
        }

        // replace the hashtags
        for (let i = 0; i < entities.hashtags.length; i++) {
            let hashtag = entities.hashtags[i];
            let link = document.createElement("a");
            link.href = "https://twitter.com/hashtag/" + hashtag.text;
            link.innerHTML = "#" + hashtag.text;

            text.innerHTML = text.innerHTML.replace("#" + hashtag.text, link.outerHTML);
        }

        // replace the urls
        for (let i = 0; i < entities.urls.length; i++) {
            let url = entities.urls[i];
            let link = document.createElement("a");
            link.href = url.expanded_url;
            link.innerHTML = url.display_url;

            text.innerHTML = text.innerHTML.replace(url.url, link.outerHTML);
        }

        return text;
    }

    function buildTweet(tweet) {
        // build the tweet
        var tweetElement = document.createElement("div");
        tweetElement.className = "tweet-wrapper";

        // build the user
        var user = buildUser(tweet);
        tweetElement.appendChild(user);

        // build the text
        var text = buildText(tweet);
        tweetElement.appendChild(text);

        return tweetElement;
    }
    
    function onEvent(data) {
        var tweet = buildTweet(data);
        
        // add the tweet to the element
        // but prepend it so that the newest tweet is at the top
        element.prepend(tweet);
        
        // if there are more than the limit, remove the last one
        if (element.children.length > config.tweetLimit) {
            element.removeChild(element.lastChild);
        }
    }

    // return the onEvent function and the id
    return onEvent;
}