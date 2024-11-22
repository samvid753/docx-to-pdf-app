#!/bin/bash


echo "Pulling the latest Docker image..."
docker pull samvidverma/docx-to-pdf-app:latest


echo "Stopping and removing any existing container..."
docker stop docx-to-pdf-app || true
docker rm docx-to-pdf-app || true


echo "Starting the Docker container..."
docker run -d -p 5000:5000 --name docx-to-pdf-app samvidverma/docx-to-pdf-app:latest

echo "Container is running at http://localhost:5000"
