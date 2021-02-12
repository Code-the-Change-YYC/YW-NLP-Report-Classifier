FROM node:12-alpine

COPY . /app
WORKDIR /app

RUN npm install -D @sanity/cli
RUN export SANITY_AUTH_TOKEN=$(cat SANITY_TOKEN)

EXPOSE 3333

CMD npm start