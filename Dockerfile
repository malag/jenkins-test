FROM python:3.7.9-alpine

ADD ./src /code

WORKDIR /code

RUN pip install -r dependences.txt

CMD ["python3", "app.py"]
