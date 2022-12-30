# Spotify Data Analysis - Album Lengths Over Time
This app interacts with the Spotify API to determine how album lengths have changed over time. The purpose of this project is to work within Python, AWS (Lambda, S3, Cloudwatch, Glue, Athena) and Terraform to build an end-to-end data pipeline that includes a data visualization as the output.

To narrow the scope of albums to analyze we choose a specific Spotify playlist to initiate the process. Then we leverage Python to interact with the Spotify API and get data about the artists in that playlist. We then interact with a different Spotify API endpoint to get data about each album for each of those artists, including track lengths and release date. Using that information we calculate the length of each of those albums. 

The output of that processing allows us to make some observations about how album lengths change over time. We visualize the results to share our findings.

## Prerequisites
You will need the following:
* Python (and the Spotipy library)
* Terraform
* AWS account
* Spotify API credentials

## Steps
1. Create a python script that will:
   * Connect to the Spotify API using the Spotipy Python library
   * Retrieve the artists that exist in a playlist (specified in the Python script)
   * Further interact with the Spotify API to obtain data about each album for each artist in the playlist, including the release year and individual track lengths
   * Calculate the total length of each album using the data from the individual tracks

2. Create Terraform scripts that will standup the AWS environment
   * The Lambda function that will run our Python script, including any needed dependencies
   * A Cloudwatch alarm will run on a cadence to pull new data about the playlist over time

3. The Lambda will save data into S3. Configure an AWS Glue crawler and use Athena to query the data in S3 as a data lake, and save the output to a new location in S3

4. Use the Athena results to generate a visualization that answers our initial question of "How are album lengths changing over time?"

## Next Steps
Now that we can analyze a given playlist, what happens if we start looking at different genres? How do album lengths change over time for pop artists vs rap artists? What other observations can we make?
