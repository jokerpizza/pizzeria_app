# Stage 1: Build
FROM node:18-alpine AS build
WORKDIR /app
# Copy package files and install
COPY package.json package-lock.json* ./
RUN npm install
# Copy source and build
COPY . .
RUN npm run build

# Stage 2: Serve static files
FROM node:18-alpine
WORKDIR /app
# Install serve to host the static files
RUN npm install -g serve
# Copy build output
COPY --from=build /app/dist ./dist
# Expose the port
EXPOSE 3000
# Start serving
CMD ["serve", "-s", "dist", "-l", "3000"]
