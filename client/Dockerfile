# Node only used for building
FROM node:12 as build

WORKDIR /app
COPY . /app

RUN npm install
RUN npm run build

FROM nginx:alpine
# Copy build folder from react to the root of nginx
COPY --from=build /app/build /usr/share/nginx/html
# replace nginx config
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
