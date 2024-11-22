#!/bin/bash

# Pull the latest Docker image
echo "Pulling the latest Docker image..."
docker pull samvidverma/docx-to-pdf-app:latest

# Stop and remove any existing container with the same name
echo "Stopping and removing any existing container..."
docker stop docx-to-pdf-app || true
docker rm docx-to-pdf-app || true

# Run the container
echo "Starting the Docker container..."
docker run -d -p 5000:5000 --name docx-to-pdf-app samvidverma/docx-to-pdf-app:latest

echo "Container is running at http://localhost:5000"
