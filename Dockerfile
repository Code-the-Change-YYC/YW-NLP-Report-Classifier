FROM python:3.8

MAINTAINER Jofred Cayabyab <jofred.cayabyab1@ucalgary.ca>

ADD . /opt/app
WORKDIR /opt/app

RUN python -m pip install -r requirements.txt
RUN python -m spacy download en_core_web_lg

EXPOSE 8000
ENV PORT=8000

CMD ENV=production uvicorn app:app --reload --port 8000 --host 0.0.0.0
