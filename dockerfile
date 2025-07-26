FROM python:3.9

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/data/processed /app/best_models /app/matrizes /app/mlruns

EXPOSE 5000

ENV PYTHONPATH=/app
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["python", "app.py"]