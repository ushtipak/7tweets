import requests
import json

url = "http://localhost:2500/tweets"

r = requests.get(url)
print("> get all tweets:\n{}".format(r.text))

r = requests.post(url, json=json.dumps({"tweet": "one tweet, such wow"}))
print("> post tweet: {}".format(r.json()))

r = requests.post(url,
                  json=json.dumps({"tweet": "second tweet, much much wow"}))
print("> post tweet: {}".format(r.json()))

r = requests.post(url, json=json.dumps({"tweet": "omg it's tweet 3, awesome"}))
print("> post tweet: {}".format(r.json()))

r = requests.get(url)
print("> get all tweets:\n{}".format(r.text))

tweet_id = 7
r = requests.get("{}/{}".format(url, tweet_id))
print("> get tweet #{}:\n{}".format(tweet_id, r.text))

tweet_id = 2
r = requests.get("{}/{}".format(url, tweet_id))
print("> get tweet #{}:\n{}".format(tweet_id, r.text))

tweet_id = 1
r = requests.delete("{}/{}".format(url, tweet_id))
print("> delete tweet #{}: {}".format(tweet_id, r.text))

tweet_id = 4
r = requests.delete("{}/{}".format(url, tweet_id))
print("> delete tweet #{}: {}".format(tweet_id, r.text))

r = requests.get(url)
print("> get all tweets:\n{}".format(r.text))
