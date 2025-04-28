# Use official Python image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy only requirements first (for better caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire app after installing dependencies
COPY . /app/

# Expose the FastAPI port
EXPOSE 8000

# Run Uvicorn with host set to 0.0.0.0 so it's accessible
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
