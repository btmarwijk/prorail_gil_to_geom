FROM node:20-alpine

# Stay as root for the setup phase so we can adjust permissions
WORKDIR /app

# Copy package files
COPY package*.json ./

# We don't run npm install here if we are using volumes for dev; 
# we let the container do it or map the volume.
# However, if you want it in the build:
RUN npm install

# Copy the rest
COPY . .

# Ensure the UID/GID we use at runtime will own these files
# (This is a safety net)
RUN chown -R 1000:1000 /app

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]