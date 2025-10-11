# Dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
EXPOSE 5000

# Run with gunicorn (production)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
