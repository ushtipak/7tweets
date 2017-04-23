FROM python:3

RUN mkdir -p /opt/7tweets
WORKDIR /opt/7tweets

COPY requirements.txt /opt/7tweets/

RUN pip install --no-cache-dir -r requirements.txt

COPY 7tweets.py storage.py /opt/7tweets/
CMD ["python", "7tweets.py"]
