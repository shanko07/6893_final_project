FROM node:latest

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY ./gatsby-theme/* ./

RUN npm install

RUN npm run build

CMD [ "npm", "run", "serve", "--", "--host", "0.0.0.0", "--port", "8457" ]
