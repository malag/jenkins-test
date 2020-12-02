FROM python:3.7-alpine

RUN apk add build-base jpeg-dev zlib-dev

ADD ./src /code

WORKDIR /code

RUN pip install -r dependences.txt

CMD ["python3", "app.py"]
