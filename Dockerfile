FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt gunicorn

RUN pip uninstall -y redis
RUN pip install redis

COPY . .
EXPOSE 5000

ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:5000", "main:app"]