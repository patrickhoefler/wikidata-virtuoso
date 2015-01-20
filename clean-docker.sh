#!/bin/bash

# Remove the containers
docker rm -f wikidata-virtuoso-download-and-process 2> /dev/null
docker rm -f wikidata-virtuoso 2> /dev/null

# Remove the image
docker rmi wikidata-virtuoso 2> /dev/null

# Remove all dangling images
docker rmi $(docker images -q --filter dangling=true) 2> /dev/null

echo "Successfully removed wikidata-virtuoso containers and images"
