FROM node:10.5.0

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

RUN install -g @vue/cli -g

COPY package.json .
COPY package-lock.json .
RUN npm install

CMD ["npm", "run", "serve"]