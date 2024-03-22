#!/bin/bash

git pull origin main
sudo docker compose -f docker-compose.yaml down
sudo docker compose -f docker-compose.yaml build
sudo docker compose -f docker-compose.yaml up -d