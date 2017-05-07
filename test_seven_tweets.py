from seven_tweets import *

import pytest

test_client = app.test_client()


def test_get_tweets():
    response = test_client.get('/tweets')
    assert response.get_data(as_text=True) == "There are no tweets :("


def test_delete_tweet():
    response = test_client.get("/tweets/100")
    assert response.get_data(as_text=True) == "There is no tweet with id 100"

