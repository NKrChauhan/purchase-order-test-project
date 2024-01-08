# Use Python image as the base image
FROM python:3.10.1

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt /app/

# Upgrade pip
RUN pip install --upgrade pip

# Install requirements
RUN pip install -r requirements.txt

# Copy project files to the container
COPY . /app/

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Set permission for entrypoint.sh
RUN chmod +x "/app/entrypoint.sh"

# Set the entrypoint for the application
ENTRYPOINT ["/app/entrypoint.sh"]
