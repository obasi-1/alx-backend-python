# Use an official Python runtime as a parent image
# Using python:3.10 as specified
FROM python:3.10-slim-buster

# Set environment variables to prevent Python from writing .pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Ensure Python output is sent straight to the terminal without buffering
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# We use --no-cache-dir to reduce the image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code to the working directory
COPY . .

# Expose the port the app runs on
# The default Django port is 8000
EXPOSE 8000

# Define the command to run your app using Gunicorn or Django's development server
# For production, Gunicorn is recommended. For this exercise, runserver is sufficient.
# The 0.0.0.0 address makes the server accessible from outside the container.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

