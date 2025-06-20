FROM python:3.12-slim

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt
RUN apt-get update && apt-get install python3-opencv  -y

WORKDIR /app-v2

COPY ./app-v2 /app-v2
WORKDIR /

ADD start.sh /
RUN chmod +x /start.sh

EXPOSE 6006

CMD ["start.sh"]