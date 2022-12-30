#!/usr/bin/env bash

# remove the current layer zips and create a working folder
rm -r deployment/layer*.zip
mkdir -p tmp/

# copy the contents of our external libraries into the new folder
cp -r venv/lib/python3.8/site-packages/requests tmp/
cp -r venv/lib/python3.8/site-packages/spotipy tmp/

# create the zip files
zip -r deployment/layer_requests.zip tmp/requests
zip -r deployment/layer_spotipy.zip tmp/spotipy

# cleanup
rm -r tmp/
