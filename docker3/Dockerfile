FROM python

WORKDIR /app


COPY . .

# Install required packages
RUN pip install --no-cache-dir pandas sqlalchemy

# Run the main script
CMD ["python", "cleanbooks.py"]
