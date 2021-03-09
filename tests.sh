#!/usr/bin/env bash

containerId=$(docker ps --filter="name=rest_rest" -q | xargs)
docker exec -it ${containerId} sh -c "cd /code & python manage.py test"
