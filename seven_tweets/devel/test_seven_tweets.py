from unittest.mock import MagicMock, patch
from seven_tweets import config
from seven_tweets.app import app
import json
with patch('pg8000.connect', new=MagicMock()):
    from seven_tweets.storage import Storage


test_client = app.test_client()


def test_get_tweets(mocker):
    mocker.patch.object(Storage, 'get_tweets')
    Storage.get_tweets.return_value = json.loads(
        """[1, "professor-chaos", "much tweet, such wow"]""")

    response = test_client.get('/tweets')
    try:
        decoded_response = json.loads(response.get_data(as_text=True))
    except json.JSONDecodeError:
        assert False
    assert type(decoded_response) == list
    assert len(decoded_response) == 3
    assert response.status_code == 200
    assert response.mimetype == 'application/json'


def test_post_tweet(mocker):
    mocker.patch.object(config, 'auth_token')
    config.auth_token = 'valid-token'

    response = test_client.post('/tweets',
                                data='{"tweet": "pytest tweeet :)"}',
                                headers={'X-Auth-Token': 'invalid-token'})
    assert response.status_code == 401
    assert response.mimetype == 'text/html'
