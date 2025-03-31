FROM python:3.9-slim AS base

RUN apt-get update && apt-get install -y \
    subversion \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000 13690

CMD ["sh", "-c", "flask run & /usr/bin/svnserve -d --foreground --listen-port=13690 -r /srv/svn/repository"]
