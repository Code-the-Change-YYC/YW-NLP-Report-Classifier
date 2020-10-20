FROM nikolaik/python-nodejs:python3.8-nodejs14

MAINTAINER Jofred Cayabyab <jofred.cayabyab1@ucalgary.ca>

ADD . /opt/app
WORKDIR /opt/app

RUN python -m pip install -r requirements.txt
RUN python -m spacy download en_core_web_lg

RUN npm install --prefix client
RUN npm install

EXPOSE 3000

CMD ["npm", "start"]
