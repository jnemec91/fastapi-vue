FROM node:lts-alpine AS build-stage

WORKDIR /app/

COPY ../frontend/package*.json ./

RUN npm install

COPY ../frontend/ .

RUN npm run build

# CMD [ "npm", "run", "serve" ]

FROM nginx:alpine AS production-build
COPY ../nginx/nginx.conf /etc/nginx/nginx.conf
RUN rm -rf /usr/share/nginx/html/*
COPY --from=build-stage /app/dist /usr/share/nginx/html

# EXPOSE 80
# ENTRYPOINT ["nginx", "-g", "daemon off;"]