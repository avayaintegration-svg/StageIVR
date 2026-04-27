# 1. Use an official Python runtime as a parent image
FROM python:3.11-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy requirements first (for caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 5. Copy app code
COPY . .

# 6. Create non-root user and set ownership
RUN useradd -m myuser && chown -R myuser /app
USER myuser

# 7. Expose port
EXPOSE 8080

# 8. Command to run your app
CMD ["python", "app.py"]
