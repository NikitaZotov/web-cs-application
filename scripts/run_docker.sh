#!/bin/bash

sudo chown $(whoami):$(whoami) /var/run/docker.sock
cd ..
docker-compose up
