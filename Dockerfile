
FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app/ /app/

EXPOSE 5000

CMD ["python", "app.py"]
