#!/bin/bash

# Directory where dependencies.zip will be moved
target_dir="layer"

# Build Docker image
docker build -t lambda-layer .

# Create container from image
docker create -ti --name dummy lambda-layer bash

# Copy python packages from container to host
docker cp dummy:/layer .

# Cleanup
docker rm -f dummy
docker rmi lambda-layer

# Check if target_dir exists, if not create it
if [ ! -d "$target_dir" ]; then
  echo "Directory $target_dir does not exist. Creating..."
  mkdir -p "$target_dir"
fi

# Zip python packages and move it to the target_dir
zip -r dependencies.zip layer
mv dependencies.zip $target_dir

# Cleanup python directory and dependencies.zip file
echo "Cleaning up..."
rm -rf layer/python