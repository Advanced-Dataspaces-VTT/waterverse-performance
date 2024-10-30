# Use an official Python runtime as a parent image
FROM python:3.11-slim
# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/
RUN apt update
RUN apt install stress -y
# Install any necessary dependencies
RUN pip3 install --no-cache-dir -r requirements.txt 
# Copy the source code into the container
COPY src/ /app

# Expose the port that the Flask app will run on
EXPOSE 5000

# Define environment variables for Flask and Python paths
ENV FLASK_APP=cputester.py
ENV PYTHONPATH=/src

# Use the environment variable ADAPTER_PORT if set
ENV TESTER_PORT 5000

# Command to run the application
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=${TESTER_PORT}"]