FROM python:3.9-slim
WORKDIR /app
RUN pip install Flask flask-cors gunicorn
COPY app_usuarios.py .
COPY usuarios.json .
# OJO: Aquí llamamos a app_usuarios:app
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app_usuarios:app