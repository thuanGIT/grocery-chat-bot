FROM ubuntu:20.04

WORKDIR /app

COPY requirements.txt ./

# Run apt-get update
RUN apt-get update

# Install C compiler (gcc)
RUN apt-get install -y build-essential 

# Install python 3.8, pip3, python3 header files, libpq header files, and pg_config
RUN apt-get install -y python3.8 python3-pip python3-dev libpq-dev

RUN pip3 install -r requirements.txt

ADD ./ ./

CMD [ "main:app", "-b", ":80" ]

ENTRYPOINT [ "gunicorn" ]