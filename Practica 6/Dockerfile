FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# Gunicorn ignorará el app.run() del final de tu código y usará el puerto correcto
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app