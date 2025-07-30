FROM python:3.12.3

# Set the working directory
WORKDIR /app

# Copy files into the container
COPY calculator.py .
COPY main.py .

RUN pip install -r requirements.txt


# Run the main script
CMD ["python", "main.py"]