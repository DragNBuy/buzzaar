FROM node:20 AS build

WORKDIR /app

RUN apt-get update && apt-get install -y python3 make g++

RUN npm install -g @angular/cli

COPY buzzaar-client/package*.json ./

RUN rm -rf node_modules package-lock.json

RUN npm install --omit=optional

COPY buzzaar-client/ .

EXPOSE 4200

CMD ["npm", "start"]

