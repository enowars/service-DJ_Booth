FROM golang:1-alpine
RUN apk add --no-cache make
WORKDIR /service/dj_booth/
ENV GOPATH /service
EXPOSE 7556
CMD make run