#!/usr/bin/env bash

# delete and recreate the working folder
rm -r ../deployment/
mkdir -p ../deployment/lambda_layer/

# copy the contents of our external libraries into the new folder
cp -r ../venv/lib/python3.8/site-packages/requests ../deployment/lambda_layer/
cp -r ../venv/lib/python3.8/site-packages/spotipy ../deployment/lambda_layer/

# create the zip files
zip -r ../deployment/requests_layer.zip ../deployment/lambda_layer/requests
zip -r ../deployment/spotipy_layer.zip ../deployment/lambda_layer/spotipy

# cleanup
rm -r ../deployment/lambda_layer/


