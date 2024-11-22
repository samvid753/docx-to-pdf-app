# Step 1: Use a base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements.txt from the app folder to the container
COPY app/requirements.txt /app/

# Step 4: Install the dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Step 5: Copy the entire application (excluding files in .dockerignore)
COPY app/ /app/

# Step 6: Expose the port your app will run on (optional if you're running a web app)
EXPOSE 5000

# Step 7: Set the command to run your application
CMD ["python", "app.py"]
