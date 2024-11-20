# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV PORT 5000

# Use Gunicorn as the production server. Adjust the worker number as necessary.
CMD ["gunicorn", "--workers=3", "--bind", "0.0.0.0:5000", "app:app"]
