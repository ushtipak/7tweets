FROM python:3

RUN mkdir -p /opt/7tweets
WORKDIR /opt/7tweets

COPY requirements.txt /opt/7tweets/

RUN pip install --no-cache-dir -r requirements.txt

COPY seven_tweets.py storage.py config.py db.py auth.py exceptions.py /opt/7tweets/
CMD ["gunicorn", "-w", "8", "-b", "0.0.0.0:2500", "seven_tweets:app"]
