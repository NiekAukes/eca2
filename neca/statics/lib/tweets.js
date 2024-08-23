function tweets(id, config = {
    "tweetLimit": 10,
}) {

    // initialize the block
    var element = document.getElementById(id);
    element.className += " tweets";
    
    function buildProfilePicture(tweet) {
        // add the image
        var img = document.createElement("img");
        img.className = "tweet-user-img";
        img.src = "/static/res/DefaultTwitterUser.png"
        img.alt = "Profile Picture";
        return img;
    }

    function buildUser(tweet) {
        if (tweet.user == undefined) {
            var user = tweet;
        } else {
            var user = tweet.user;
        }


        // create the wrapper
        var wrap = document.createElement("div");
        wrap.className = "tweet-user";

        // add the name
        var name = document.createElement("p");
        name.className = "tweet-user-name";
        name.innerHTML = user.name
        
        wrap.appendChild(name);

        // add the screen name / handle / username
        var screenName = document.createElement("a");
        screenName.className = "tweet-user-screen-name";
        screenName.innerHTML = "@" + user.screen_name;
        screenName.href = "https://twitter.com/" + user.screen_name;
        wrap.appendChild(screenName);

        return wrap;
    }

    function buildText(tweet) {
        var text = document.createElement("p");
        text.className = "tweet-text";
        text.innerHTML = tweet.text;

        // use the intities to build links
        if (tweet.entities == undefined) {
            return text;
        }
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

        // build the profile picture
        var profilePicture = buildProfilePicture(tweet);
        tweetElement.appendChild(profilePicture);

        // make another div for the user and text
        var userText = document.createElement("div");
        userText.className = "tweet-user-text";

        // build the user
        var user = buildUser(tweet);
        userText.appendChild(user);

        // build the text
        var text = buildText(tweet);
        userText.appendChild(text);

        // add the user and text to the tweet
        tweetElement.appendChild(userText);

        return tweetElement;
    }
    
    function onEvent(data) {
        if (data == undefined) {
            // remove all the tweets
            for (let i = 0; i < element.children.length; i++) {
                element.removeChild(element.children[i]);
            }
            return; 
        }
        
        var tweet = buildTweet(data);
        
        // add the tweet to the element
        // but prepend it so that the newest tweet is at the top
        element.prepend(tweet);
        
        // if there are more than the limit, remove the last one
        if (element.children.length > config.tweetLimit) {
            element.removeChild(element.lastChild);
        }
    }

    // return the onEvent function
    return onEvent;
}