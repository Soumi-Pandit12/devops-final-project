FROM python:3.9-slim

WORKDIR /app

# Copy requirements from the app folder
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the app folder into the container
COPY app/ .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]