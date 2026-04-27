FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Flask runs on 5000 inside the container
EXPOSE 5000

CMD ["python", "quicknotes-app/app.py"]