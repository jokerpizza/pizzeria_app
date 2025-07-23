FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend /app
ENV PYTHONPATH=/app
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","10000"]
