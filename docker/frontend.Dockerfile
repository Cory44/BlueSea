# syntax=docker/dockerfile:1.6

FROM node:22-alpine

ENV NODE_ENV=development

WORKDIR /app

COPY frontend/package.json frontend/package-lock.json ./

RUN npm install

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
