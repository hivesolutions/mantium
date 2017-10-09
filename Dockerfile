FROM hivesolutions/python:latest

LABEL version="1.0"
LABEL maintainer="Hive Solutions <development@hive.pt>"

EXPOSE 8080

ENV LEVEL INFO
ENV SERVER netius
ENV SERVER_ENCODING gzip
ENV HOST 0.0.0.0
ENV PORT 8080
ENV MONGOHQ_URL mongodb://localhost
ENV PYTHONPATH /src

ADD requirements.txt /
ADD src /src

RUN pip3 install -r /requirements.txt && pip3 install --upgrade netius

CMD ["/usr/bin/python3", "/src/mantium/main.py"]
