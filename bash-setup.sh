#!/bin/bash

# Build Docker image
docker build -t username/docx-to-pdf .

# Run Docker container
docker run -d -p 5000:5000 username/docx-to-pdf
