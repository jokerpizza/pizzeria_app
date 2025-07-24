# Stage 1: Build
FROM node:18-alpine AS build
WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile
COPY . .
RUN yarn build

# Stage 2: Serve static files
FROM node:18-alpine
WORKDIR /app
# Install serve to serve the built files
RUN yarn global add serve
# Copy build output
COPY --from=build /app/dist ./dist
# Expose the port serve will run on
EXPOSE 3000
# Run serve to host the static files
CMD ["serve", "-s", "dist", "-l", "3000"]
