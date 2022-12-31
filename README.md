# Spotify Data Analysis - Album Lengths Over Time
This app interacts with the Spotify API to determine how album lengths have changed over time. The purpose of this project is to work within Python, AWS and Terraform to build an end-to-end data pipeline that produces data visualizations as the end product.

To analyze albums over time we need to define a nice sample size. We get a popular Spotify playlist (interacting with the API via Python) to give us a nice assortment of artists. Then we use a different API endpoint to get data about each album for those artists. We are most interested in the track lengths and release dates. Using that information we then have to calculate the length of each of those albums on our own. 

The output of that processing allows us to make some observations about how album lengths change over time. We visualize the results to share our findings. Changing the playlist used as the source of data (and thus the genre) might produce different observations.

## Prerequisites
You will need the following:
* Python
* Terraform
* AWS account
* Spotify API credentials

## Steps
1. Create a python script that will:
   * Connect to the Spotify API using the Spotipy Python library
   * Retrieve the artists that exist in a playlist (specified in the Python script)
   * Further interact with the Spotify API to obtain data about each album for each artist in the playlist, including the release year and individual track lengths
   * Calculate the total length of each album using the data from the individual tracks

2. Create Terraform scripts that will standup the AWS environment:
   * S3 buckets to store our data files as well as our Lambda code
   * A Lambda function that will run our Python script, including any needed dependencies
   * A Cloudwatch alarm will run on a cadence to pull new data about the playlist over time

3. The Lambda will save data into S3. Configure an AWS Glue crawler and use Athena to query the data in S3 as a data lake, and save the output to a new location in S3

4. Use the Athena results to generate a visualization that answers our initial question of "How are album lengths changing over time?"

## Next Steps
Now that we can analyze a given playlist, what happens if we start looking at different genres? How do album lengths change over time for pop artists vs rap artists? What other observations can we make?
