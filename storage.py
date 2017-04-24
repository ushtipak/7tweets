server_name = "professor-chaos"


class Storage(object):
    _tweets = []
    _tweet_count = 0

    @classmethod
    def get_tweets(cls):
        """Return all tweets."""
        # TODO: Should method return 204 No Content if there are no tweets?
        return cls._tweets

    @classmethod
    def post_tweet(cls, body):
        """Create tweet based on given body, store it and increment count."""
        cls._tweet_count += 1
        tweet = {"id": cls._tweet_count,
                 "name": server_name,
                 "tweet": body}
        cls._tweets.append(tweet)
        return "added!"

    @classmethod
    def get_tweet(cls, tweet_id):
        """Return tweet (if exists) with given ID."""
        return [tweet for tweet in cls._tweets if tweet["id"] == tweet_id] or \
               "no tweet #{}".format(tweet_id)

    @classmethod
    def delete_tweet(cls, tweet_id):
        """Delete tweet (if exists) with given ID."""
        try:
            # check if tweet with given id exists
            # if so - remove it from tweet list based on it's index
            del cls._tweets[([cls._tweets.index(tweet) for tweet
                              in cls._tweets if tweet["id"] == tweet_id][0])]
            return "deleted!"
        except IndexError:
            # if it doesn't exist - return adequate message
            return "no tweet #{}".format(tweet_id)
