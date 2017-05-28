from seven_tweets.auth import is_authorized as requires_auth
from seven_tweets.exceptions import handles_exceptions
from flask import Flask, request, jsonify
from seven_tweets.storage import Storage
from datetime import datetime
import json


app = Flask(__name__)


@app.before_first_request
def initialize_database():
    """Make sure DB has tweets table."""
    Storage.initialize()


@app.route("/tweets")
@handles_exceptions
def get_tweets():
    """Display all tweets."""
    tweets = Storage.get_tweets()
    return jsonify(tweets) if tweets else ("There are no tweets :(", 404)


@app.route("/tweets", methods=['POST'])
@handles_exceptions
@requires_auth
def post_tweet():
    """Store tweet (from provided JSON tweet body)."""
    tweet_body = json.loads(request.get_json())["tweet"]
    return jsonify(Storage.post_tweet(tweet_body))


@app.route("/tweets/<int:tweet_id>")
@handles_exceptions
def get_tweet(tweet_id):
    """Display tweet (if exists) with given ID."""
    tweet = Storage.get_tweet(tweet_id)
    return jsonify(tweet) if tweet else ("There is no tweet with id {}".
                                         format(tweet_id), 404)


@app.route("/tweets/<int:tweet_id>", methods=['PUT'])
@handles_exceptions
@requires_auth
def update_tweet(tweet_id):
    """Update tweet (if exists) with given ID and new tweet body."""
    tweet_body = json.loads(request.get_json())["tweet"]
    updated = Storage.update_tweet(tweet_body, tweet_id)
    return jsonify(updated) if updated else ("There is no tweet with id {}".
                                             format(tweet_id), 404)


@app.route("/tweets/<int:tweet_id>", methods=['DELETE'])
@handles_exceptions
@requires_auth
def delete_tweet(tweet_id):
    """Delete tweet (if exists) with given ID."""
    deleted = Storage.delete_tweet(tweet_id)
    return jsonify(deleted) if deleted else ("There is no tweet with id {}".
                                             format(tweet_id), 404)


@app.route("/search", methods=['GET'])
@handles_exceptions
def search_tweets():
    """Performs tweet search in local DB and optionally on remote nodes."""
    tweets = Storage.search_tweets(**json.loads(request.get_json()))
    return jsonify(tweets) if tweets else ("There are no tweets :(", 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2500, debug=True)
