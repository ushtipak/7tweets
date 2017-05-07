import pg8000
import config


def initialize():
    """Creates initial tweets table if missing."""
    connection = pg8000.connect(**config.DB_CONFIG)
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tweets
        (id SERIAL PRIMARY KEY, name VARCHAR(20) NOT NULL, tweet TEXT);
        """)
    cursor.close()
    connection.commit()
