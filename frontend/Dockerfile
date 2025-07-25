FROM node:20-alpine

WORKDIR /frontend

COPY package*.json ./

RUN npm install -g @angular/cli@20.1.3

RUN npm install

COPY . .

EXPOSE 4200

CMD ["ng", "serve", "--host", "0.0.0.0"]

