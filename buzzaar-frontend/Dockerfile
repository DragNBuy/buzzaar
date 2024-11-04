FROM node:20 AS build

WORKDIR /app

RUN apt-get update && apt-get install -y python3 make g++

COPY buzzaar-ui/package*.json ./

RUN npm install --omit=optional

RUN npm install -g @angular/cli

COPY buzzaar-ui/ .

EXPOSE 4200

CMD ["npm", "start"]

