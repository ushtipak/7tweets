#!/usr/bin/python3

from flask import Flask, request, jsonify
from storage import Storage
import json


app = Flask(__name__)


@app.route("/tweets")
def get_tweets():
    """Display all tweets."""
    return jsonify(Storage.get_tweets())


@app.route("/tweets", methods=['POST'])
def post_tweet():
    """Store tweet (from provided JSON tweet body)."""
    return jsonify(Storage.post_tweet(json.loads(request.get_json())["tweet"]))


@app.route("/tweets/<int:tweet_id>")
def get_tweet(tweet_id):
    """Display tweet (if exists) with given ID."""
    return jsonify(Storage.get_tweet(tweet_id))


@app.route("/tweets/<int:tweet_id>", methods=['DELETE'])
def delete_tweet(tweet_id):
    """Delete tweet (if exists) with given ID."""
    return jsonify(Storage.delete_tweet(tweet_id))


if __name__ == "__main__":
    app.run(port=2500, debug=True)
