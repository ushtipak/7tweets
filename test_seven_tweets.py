from seven_tweets import *

import pytest

test_client = app.test_client()


def test_get_tweets():
    response = test_client.get('/tweets')
    assert response.get_data(as_text=True) == "[]\n"
