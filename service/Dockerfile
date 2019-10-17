FROM golang:buster
RUN apt update && apt install -y make gcc
WORKDIR /service/dj_booth/
ENV GOPATH /service
EXPOSE 7556
CMD make run