FROM node:14.8.0-alpine3.12

WORKDIR .

COPY package.json ./
COPY package-lock.json ./

RUN npm install
RUN npm install react-scripts@3.4.3 -g

CMD ["pwd"]
COPY . ./

EXPOSE 3000

CMD ["npm", "start"]

# FROM node:14.8.0-alpine3.12 as builder
# RUN mkdir -p /usr/src/app
# WORKDIR /usr/src/app
# ENV PATH /usr/src/app/node_modules/.bin:$PATH
# COPY package*.json ./
# RUN npm install --silent
# RUN npm install react-scripts@3.4.3 -g --silent
# COPY . /usr/src/app
# RUN npm run build
 
# FROM nginx:1.14.1-alpine
# RUN apk add --no-cache jq
# RUN rm -rf /etc/nginx/conf.d
# COPY conf /etc/nginx
# COPY --from=builder /usr/src/app/build /usr/share/nginx/html
# COPY docker-entrypoint.sh generate_config_js.sh /
# RUN chmod +x docker-entrypoint.sh generate_config_js.sh
 
# ENTRYPOINT ["/docker-entrypoint.sh"]

