#!/bin/bash

# Build the main image
docker build --tag=wikidata-virtuoso .

# Download and process the Wikidata dump
docker run \
  --rm \
	--name=wikidata-virtuoso-download-and-process \
	-v $PWD/cache:/usr/src/app/cache \
	-v $PWD/output:/usr/src/app/output \
	wikidata-virtuoso:latest \
	./download-and-process.py

# Start Virtuoso
docker rm -f wikidata-virtuoso 2> /dev/null
docker run \
	--name=wikidata-virtuoso \
	-v $PWD/cache:/usr/src/app/cache \
	-v $PWD/output:/usr/src/app/output \
	-v $PWD/virtuoso:/var/lib/virtuoso-opensource-6.1/db \
  -p 8890:8890 \
	-d \
  --restart=always \
	wikidata-virtuoso:latest

# Import the processed Wikidata dump into Virtuoso
docker exec wikidata-virtuoso ./import-dump.sh
