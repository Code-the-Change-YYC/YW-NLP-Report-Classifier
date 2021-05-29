# Node only used for building
FROM node:12 as build

COPY package.json /app/package.json
WORKDIR /app

RUN npm install

COPY . /app

# Change to Sanity production dataset
RUN sed -i 's/development/production/g' .env

RUN npm run build

FROM nginx:alpine
RUN apk add --no-cache bash
# Copy build folder from react to the root of nginx
COPY --from=build /app/build /usr/share/nginx/html
# replace nginx config
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/templates/form.template
