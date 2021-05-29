FROM node:12-alpine

WORKDIR /app
COPY package.json package.json
COPY package-lock.json package-lock.json

RUN npm ci

COPY . .

RUN export SANITY_AUTH_TOKEN=$(cat keys/SANITY_TOKEN)

# Change to Sanity production dataset
RUN sed -i 's/dataset: "development"/dataset: "production"/g' sanity.json

CMD npm run prod
