FROM ubuntu:20.04

WORKDIR /app

COPY requirements.txt ./

RUN apt-get update && apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

ADD ./ ./

CMD [ "main:app" ]

ENTRYPOINT [ "gunicorn" ]