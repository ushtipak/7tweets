from flask import Flask, request, jsonify
from storage import Storage
import json
import db

app = Flask(__name__)


@app.before_first_request
def initialize_database():
    """Make sure DB has tweets table."""
    db.initialize()


@app.route("/tweets")
def get_tweets():
    """Display all tweets."""
    tweets = Storage.get_tweets()
    return jsonify(tweets) if tweets else ("There are no tweets :(", 404)


@app.route("/tweets", methods=['POST'])
def post_tweet():
    """Store tweet (from provided JSON tweet body)."""
    tweet_body = json.loads(request.get_json())["tweet"]
    return jsonify(Storage.post_tweet(tweet_body))


@app.route("/tweets/<int:tweet_id>")
def get_tweet(tweet_id):
    """Display tweet (if exists) with given ID."""
    tweet = Storage.get_tweet(tweet_id)
    return jsonify(tweet) if tweet else ("There is no tweet with id {}".
                                         format(tweet_id), 404)


@app.route("/tweets/<int:tweet_id>", methods=['DELETE'])
def delete_tweet(tweet_id):
    """Delete tweet (if exists) with given ID."""
    deleted = Storage.delete_tweet(tweet_id)
    return jsonify(deleted) if deleted else ("There is no tweet with id {}".
                                             format(tweet_id), 404)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2500, debug=True)
