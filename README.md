# Spotify Data Analysis - Album Lengths Over Time

This app interacts with the Spotify API to determine how album lengths have changed over time. The purpose of this project is to work within Python, AWS and Terraform to build an end-to-end data pipeline that produces data visualizations as the end product.

To analyze albums over time we need to define a nice sample size. We get a popular Spotify playlist (interacting with the API via Python) to give us a nice assortment of artists. Then we use a different API endpoint to get data about each album for those artists. We are most interested in the track lengths and release dates. Using that information we then have to calculate the length of each of those albums on our own.

The output of that processing allows us to make some observations about how album lengths change over time. We visualize the results to share our findings. Changing the playlist used as the source of data (and thus the genre) might produce different observations.

## High-Level Steps

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

## Prerequisites

You will need the following:

* Python
* Terraform
* AWS account
* Spotify API credentials

## Setup

### Create a terraform.tfvars file

A set of environment variables are required in order to Terraform to do what it needs to do. This includes the credentials to connect to your AWS account and the Spotify API.

As this is sensitive information, we do not want to include it in the repo. So you would need to create a file at  `./tf/terraform.tfvars`

Inside of that file we need to define our credentials for both AWS and Spotify 
```
AWS_ACCESS_KEY_ID={YOUR_KEY}
AWS_SECRET_ACCESS_KEY={YOUR_SECRET}
SPOTIPY_CLIENT_ID={YOUR_CLIENT_ID}
SPOTIPY_CLIENT_SECRET={YOUR_SECRET}
```

Make sure that this .tfvars file is included in the .gitignore, we do not want to check this into the repo.

### Run the terraform scripts
The variables that are now defined in the .tfvars file are used in the `./tf/variable.tf` file. Now that Terraform is able to authenticate to AWS we can run Terraform
```
cd /tf
terraform init
terraform plan
```

If all goes well then you go can ahead and apply the changes using `terraform apply`. This should create the s3 paths, the Lambda, and a Cloudwatch rule that will run the Lambda on a weekly schedule.

As the Lambda runs each week the results of the script will be saved into a file in S3. From that point we can use the data to start making observations and visualizations around the data, and see how album lengths are changing over time.

### Create a local .env file
In order to connect to S3 to do analysis of the files and create some visualizations, we need a way to authenticate to AWS. The way I chose to do this is to utilize
the `os` and `dotenv` libraries to read my access key and secret from a local .env file. As this is sensitive info I have added the .env file to my .gitignore.

Inside my Python scripts I just call `load_dotenv()`. By default that will look for environment variables to load within a file named .env, which exists in the root of my project. The contents of that file are just these variables:
```
AWS_ACCESS_KEY_ID={MY_ACCESS_KEY}
AWS_SECRET_ACCESS_KEY={MY_SECRET_KEY}
```

By calling `load_dotenv()` in my Python scripts, I can now access those values using the `os.getlogic()' command:
```
aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY") 
```

## Next Steps / Further Improvements

### Further Observations

Now that we can analyze a given playlist, what other observations can be made? Some examples I have considered include:

* What happens if we start looking at different genres?
* How do album lengths change over time for pop artists vs rap artists?
* What if we evaluate classic rock artists vs current rock artists?

### Technical Improvement Ideas

* Move the way we authenticate the app to an IAM role instead of using an access key
* Terraform:
  * Move the spotify API credentials into secrets manager
  * Move the playlist ID into the lambda environment variables
* ETL the s3 data into a database/data lake (Glue/DynamoDB?)
* Visualize data from the database (Python)
