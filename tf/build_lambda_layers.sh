#!/usr/bin/env bash

# delete and recreate the working folder
rm -r ../deployment/*layer*
mkdir -p ../deployment/lambda_layers/

# copy the contents of our external libraries into the new folder
cp -r ../venv/lib/python3.8/site-packages/requests ../deployment/lambda_layers/
cp -r ../venv/lib/python3.8/site-packages/spotipy ../deployment/lambda_layers/

# create the zip files
zip -r ../deployment/layer_requests.zip ../deployment/lambda_layers/requests
zip -r ../deployment/layer_spotipy.zip ../deployment/lambda_layers/spotipy

# cleanup
rm -r ../deployment/lambda_layers/
