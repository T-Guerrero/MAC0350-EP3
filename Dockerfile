FROM python:3.8.5

ENV PORT=8000 \
  HOST=0
WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python manage.py runserver ${HOST}:${PORT}