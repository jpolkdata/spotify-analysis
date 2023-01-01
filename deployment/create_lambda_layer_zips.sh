#!/usr/bin/env bash

##################################################
# Generate the lambda layer zip files
##################################################

# remove the current layer zips and create a working folder
rm -r layer*.zip
mkdir -p python/

# create the requests zip
pip install requests -t python/
zip -r layer_requests.zip python/
rm -r python/*

# create the spotipy zip
pip install spotipy -t python/
zip -r layer_spotipy.zip python/
rm -r python/


# NOTE: apply the terraform plan to deploy the files out to AWS
