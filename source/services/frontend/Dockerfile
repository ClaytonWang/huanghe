# syntax=docker/dockerfile:1.4

FROM node:16.16.0-slim AS front

WORKDIR /www

COPY package*.json yarn.lock ./

RUN yarn --registry=https://registry.npmmirror.com

COPY . .

ENV NODE_ENV production

RUN yarn build

FROM nginx:stable-alpine

COPY deploy/conf.d/default.conf /etc/nginx/conf.d/default.conf

COPY deploy/nginx.conf /etc/nginx/nginx.conf

COPY --from=front /www/dist /usr/share/nginx/html/www

ENTRYPOINT ["nginx", "-g", "daemon off;"]
