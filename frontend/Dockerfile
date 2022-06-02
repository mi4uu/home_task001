FROM node:16-alpine

RUN npm install -g pnpm
WORKDIR /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ADD . .

RUN pnpm install

ENTRYPOINT ["/entrypoint.sh"]

CMD ["npm", "run", "dev"]

