#!/bin/sh

docker build -t fint-assignment .
docker run -p8000:8000 fint-assignment