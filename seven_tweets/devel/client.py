from seven_tweets import config
import requests
import json


url = "http://localhost:2500/tweets"
auth = {'X-Auth-Token': config.auth_token}

r = requests.get(url)
print("> get all tweets:\n{}".format(r.text))

r = requests.post(url,
                  json=json.dumps({"tweet": "one tweet, such wow"}),
                  headers=auth)
print("> post tweet: {}".format(r.json()))

r = requests.post(url,
                  json=json.dumps({"tweet": "second tweet, much much wow"}),
                  headers=auth)
print("> post tweet: {}".format(r.json()))

r = requests.post(url,
                  json=json.dumps({"tweet": "omg it's tweet 3, awesome"}),
                  headers=auth)
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
r = requests.delete("{}/{}".format(url, tweet_id), headers=auth)
print("> delete tweet #{}: {}".format(tweet_id, r.text))

tweet_id = 2
r = requests.put("{}/{}".format(url, tweet_id),
                 json=json.dumps({"tweet": "such a nice update, many wow"}),
                 headers=auth)
print("> update tweet: {}".format(r.json()))

tweet_id = 4
r = requests.delete("{}/{}".format(url, tweet_id))
print("> delete tweet #{}: {}".format(tweet_id, r.text))

r = requests.get(url)
print("> get all tweets:\n{}".format(r.text))


r = requests.get(url.replace("tweets", "search"),
                 json=json.dumps({"content": "wow",
                                  "created_from": "2016-05-20",
                                  "all": True}))
print("> search tweets: {}".format(r.text))

