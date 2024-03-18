FROM python:3.11.7-slim

WORKDIR /app

COPY . /app

# Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD uvicorn main:app --port=8080 --host=0.0.0.0

