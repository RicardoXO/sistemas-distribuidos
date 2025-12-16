FROM python:3.9-slim
WORKDIR /app
RUN pip install Flask flask-cors gunicorn
COPY app_clima.py .
COPY clima.json .
# OJO: Aquí llamamos a app_clima:app
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app_clima:app