# syntax=docker/dockerfile:1

# Build the time database
FROM python:3-alpine

WORKDIR /data

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY convert.py ./
ADD https://github.com/masto/literature-clock/raw/master/litclock_annotated.csv .
RUN mkdir times
RUN python3 convert.py

# Build the production image
FROM python:3-alpine

WORKDIR /app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY clock.py lookup.py word_clock.py ./
COPY times/ ./times/

ENTRYPOINT ["python3", "clock.py"]
