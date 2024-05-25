# Use an official Python runtime as a parent image
FROM python:3.11-slim

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=OPENAI_API_KEY

# Set the working directory in the container to /app
WORKDIR /app

# Add just the requirements into the container at /app
COPY ./src/requirements.txt .

# Install Git and any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y git
RUN pip install --no-cache-dir -r requirements.txt

# Add the current directory contents into the container at /app
COPY ./src .

# Make port 80 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "server.py"]