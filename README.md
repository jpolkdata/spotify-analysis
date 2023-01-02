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
   * A Lambda function that will run our Python script
   * External Python libraries are created as Lambda layers
   * IAM role and policies to allow the Lambda to be executed
   * A Cloudwatch alarm to invoke the lambda on a schedule

TO DO:
   * Terraform: 
      * Move the spotify API credentials into secrets manager
      * Move the playlist ID into the lambda environment variables
   * ETL the s3 data into a database/data lake (Glue/DynamoDB?)
   * Visualize data from the database (Python)

## Next Steps
Now that we can analyze a given playlist, what other observations can be made? Some examples I have considered include:
   * What happens if we start looking at different genres? 
   * How do album lengths change over time for pop artists vs rap artists? 
   * What if we evaluate classic rock artists vs current rock artists?
