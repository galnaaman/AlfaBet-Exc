# Use the official Redis image as the base image
FROM redis

# Copy the custom configuration file into the container
COPY redis.conf /usr/local/etc/redis/redis.conf

# Command to run Redis server with the custom configuration file
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]
