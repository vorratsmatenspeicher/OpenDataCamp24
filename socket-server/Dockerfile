FROM node:20

WORKDIR /usr/src/app

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=OPENAI_API_KEY

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 8080
EXPOSE 5000

CMD ["node", "index.js"]
