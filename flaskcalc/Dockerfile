# Use an official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy app files
COPY . /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Expose the port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
