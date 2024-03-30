# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Run database initialization, migration, and upgrade
# RUN flask db init
# RUN flask db migrate -m "Initial migration"
# RUN flask db upgrade

# Expose the port on which the Flask app will run
EXPOSE 8080

# Command to run the Flask application
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
