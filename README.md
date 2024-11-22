# DOCX-TO-PDF Flask Application

This project is a simple web application built using Flask that allows users to convert DOCX files to PDF. The application is containerized using Docker and can be deployed using Kubernetes, Render, or other platforms.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Deployment](#deployment)
- [Kubernetes Setup](#kubernetes-setup)
- [Contributing](#contributing)

## Project Overview

This application provides a web interface for converting DOCX files to PDF. It uses the `python-docx` library to read DOCX files and `reportlab` to generate PDFs. The app is built with Flask and is fully containerized using Docker.

## Features

- Convert DOCX files to PDF
- Simple web interface for file uploads
- Dockerized application for easy deployment
- Kubernetes deployment options for scaling
- Hosted on Render for easy access

## Technologies Used

- **Flask**: A micro web framework for Python
- **Python 3.9**: The version of Python used to build the application
- **Docker**: Containerization for easy deployment
- **Kubernetes**: For orchestration and scaling
- **Render**: For hosting the application
- **Docker Compose**: For multi-container Docker applications

## Setup

To set up this project locally, follow these steps:

### Prerequisites

- Install Docker on your system (for containerization)
- Install `kubectl` and set up Kubernetes (for deployment)


### Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/docx-to-pdf-app.git
cd docx-to-pdf-app
Docker Setup
Build Docker Image: To build the Docker image, run the following command:

bash
Copy code
docker build -t docx-to-pdf-app .
Run Docker Container: To run the container locally:

bash
Copy code
docker run -d -p 5000:5000 docx-to-pdf-app
Visit http://localhost:5000 to access the app.

Install Dependencies
Ensure all dependencies are installed:

bash
Copy code
pip install -r app/requirements.txt
Deployment
Kubernetes Setup
Create a Kubernetes Deployment File (k8s-deployment.yml):
yaml
Copy code
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docx-to-pdf-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: docx-to-pdf-app
  template:
    metadata:
      labels:
        app: docx-to-pdf-app
    spec:
      containers:
        - name: docx-to-pdf-app
          image: samvidverma/docx-to-pdf-app:latest
          ports:
            - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: docx-to-pdf-app-service
spec:
  selector:
    app: docx-to-pdf-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 5000
  type: LoadBalancer
Create an Ingress File (k8s-ingress.yml):
yaml
Copy code
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: docx-to-pdf-app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: <YOUR_DOMAIN>.com
      http:
        paths:
        - path: /
          pathType: Prefix
          backend:
            service:
              name: docx-to-pdf-app-service
              port:
                number: 80


Steps for Contributing:
Fork the repository
Create a new branch (git checkout -b feature-name)
Commit your changes (git commit -am 'Add new feature')
Push to the branch (git push origin feature-name)
Create a pull request
