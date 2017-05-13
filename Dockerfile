FROM python:3

RUN mkdir -p /opt/7tweets
WORKDIR /opt/7tweets

COPY requirements.txt /opt/7tweets/

RUN pip install --no-cache-dir -r requirements.txt

COPY seven_tweets.py storage.py config.py db.py /opt/7tweets/
CMD ["python", "seven_tweets.py"]
