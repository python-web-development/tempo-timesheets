# Use an official lightweight Python image.
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for the port and set a default value
ENV PORT=5000

# Run uvicorn to serve the application. Adjust host and port as necessary.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
