FROM node:24
WORKDIR /app

COPY package*.json ./
COPY . .

RUN npm i

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]