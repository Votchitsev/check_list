FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ['python3', 'manage.py', '3000']
