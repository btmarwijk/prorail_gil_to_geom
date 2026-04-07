FROM python:3.12
WORKDIR /app

# Install dependencies
# We copy requirements from the local 'app' folder
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything FROM the local 'app' folder TO the container '/app'
COPY . .

# Set PYTHONPATH to /app/src so 'import src' works
ENV PYTHONPATH=/app/src
EXPOSE 8000