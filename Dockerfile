FROM python:3.6.10

MAINTAINER Jofred Cayabyab <jofred.cayabyab1@ucalgary.ca>

WORKDIR /opt/app

ADD ./requirements.txt /opt/app/requirements.txt

RUN python -m pip install -r requirements.txt
RUN python -m spacy download en_core_web_lg
RUN python -m nltk.downloader wordnet
RUN python -m nltk.downloader averaged_perceptron_tagger

ADD . /opt/app
