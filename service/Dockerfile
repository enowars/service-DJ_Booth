FROM golang:buster
RUN apt-get update && apt-get install -y make gcc
WORKDIR /service/dj_booth/
ENV GOPATH /service
EXPOSE 7556
CMD make run