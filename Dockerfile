FROM python:3.12-slim

RUN mkdir /app

WORKDIR /app

RUN apt-get update \ 
    && apt upgrade -y \ 
    && apt install -y python3-pip

#COPY * /app/
COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD [ "fastapi", "dev", "app.py"]