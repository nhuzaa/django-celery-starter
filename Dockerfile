FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install setuptools first
RUN pip install --upgrade pip setuptools

# Copy requirements and install Python dependencies using pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Run migrations and seed the database
CMD ["sh", "-c", "python manage.py migrate && python seed_data.py && python manage.py runserver 0.0.0.0:8000"] 