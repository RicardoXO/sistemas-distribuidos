FROM python:3.9-slim
WORKDIR /app
RUN pip install Flask gunicorn
COPY index.html .
COPY style.css .
COPY app_frontend.py .
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app_frontend:app