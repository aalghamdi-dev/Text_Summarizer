FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /Project1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Main.py .

CMD ["python", "Main.py"]
