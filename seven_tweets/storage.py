from seven_tweets import config
import functools
import pg8000


def uses_db(fn):
    @functools.wraps(fn)
    def wrapper(cls, *args, **kwargs):
        cursor = cls._connection.cursor()
        query = fn(cls, cursor, *args, **kwargs)
        cursor.close()
        cls._connection.commit()
        return query
    return wrapper


class Storage:
    _connection = pg8000.connect(**config.DB_CONFIG)

    @classmethod
    @uses_db
    def initialize(cls, cursor):
        """Creates initial tweets table if missing."""
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tweets
            (id SERIAL PRIMARY KEY, name VARCHAR(20) NOT NULL, tweet TEXT);
            """)

    @classmethod
    @uses_db
    def get_tweets(cls, cursor):
        """Return all tweets."""
        cursor.execute(
            """
            SELECT id, name, tweet FROM tweets
            """)
        return cursor.fetchall()

    @classmethod
    @uses_db
    def post_tweet(cls, cursor, tweet_body):
        """Store tweet (based on given body and 'server name') in DB."""
        cursor.execute(
            """
            INSERT INTO tweets (name, tweet)
            VALUES ( %s, %s ) RETURNING id, name, tweet
            """, (config.app_server, tweet_body)
        )
        return cursor.fetchone()

    @classmethod
    @uses_db
    def get_tweet(cls, cursor, tweet_id):
        """Return tweet (if exists) with given ID."""
        cursor.execute(
            """
            SELECT * FROM tweets WHERE id = %s
            """, (tweet_id, )
        )
        return cursor.fetchone()

    @classmethod
    @uses_db
    def update_tweet(cls, cursor, tweet_body, tweet_id):
        """Update tweet in DB based on 'server name', tweet ID and new body."""
        cursor.execute(
            """
            UPDATE tweets SET tweet = %s
            WHERE id = %s AND name = %s RETURNING id, name, tweet
            """, (tweet_body, tweet_id, config.app_server)
        )
        return cursor.fetchone()

    @classmethod
    @uses_db
    def delete_tweet(cls, cursor, tweet_id):
        """Store tweet (based on given body and 'server name') in DB."""
        cursor.execute(
            """
            DELETE FROM tweets WHERE id = %s RETURNING id, name, tweet
            """, (tweet_id, )
        )
        return cursor.fetchone()
