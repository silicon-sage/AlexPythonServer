FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt gunicorn

RUN pip uninstall -y redis
RUN pip install redis

COPY . .
EXPOSE 5000

# Use gunicorn instead of Flask's development server
# -w 4: means 4 worker processes
# -b 0.0.0.0:5000: binds to all interfaces on port 5000
# main:app - assumes your Flask app is called 'app' in main.py
CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "main:app"]