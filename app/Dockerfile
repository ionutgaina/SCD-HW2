FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1
COPY . .
EXPOSE 5000
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${APP_PORT:-5000}"]
