FROM python:3.13-slim
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY recogniser.py /app/recogniser.py
CMD ["python", "-u", "/app/recogniser.py"]
