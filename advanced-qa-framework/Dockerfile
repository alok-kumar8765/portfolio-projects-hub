# Use official Microsoft Playwright Python base image
FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

# Set working directory inside the container
WORKDIR /app

# Copy dependency manifest first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the framework source code into the container
COPY . .

# Set environment variables for headless execution
ENV ENV=dev
ENV HEADLESS=true

# Command to execute pytest inside the container
CMD ["pytest", "-v", "--browser", "chromium"]