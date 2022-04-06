#!/bin/bash

mkdir $(grep -v '^#' .env )
cd ./todo_app
poetry run gunicorn --preload wsgi:start -b 0.0.0.0:80