FROM python

WORKDIR /app

# Copy all files into the container
COPY . .

# Install required packages
RUN pip install --no-cache-dir pandas sqlalchemy

# Run the main script
CMD ["python", "cleanbooks.py"]
