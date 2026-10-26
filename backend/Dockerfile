FROM node:20-slim

# Install C++ compiler (g++), Java (default-jdk), and clean up cache
RUN apt-get update && apt-get install -y --no-install-recommends \
    g++ \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency files first for layer caching
COPY package*.json ./

# Install production dependencies
RUN npm install --omit=dev

# Copy backend source code
COPY . .

# Render exposes PORT dynamically (fallback to 8080)
ENV PORT=8080
EXPOSE 8080

CMD ["node", "server.js"]