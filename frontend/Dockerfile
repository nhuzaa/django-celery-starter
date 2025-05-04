# Build stage
FROM node:18-alpine

WORKDIR /app

# Add environment variables for hot reloading
ENV CHOKIDAR_USEPOLLING=true
ENV WATCHPACK_POLLING=true
ENV FAST_REFRESH=true

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

# Start the development server with hot reloading
CMD ["npm", "start"] 