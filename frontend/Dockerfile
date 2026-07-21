FROM node:20-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
# 🔥 DEBUG
RUN npm run build && ls -la && ls -la dist

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
