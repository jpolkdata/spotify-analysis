from dotenv import load_dotenv
import os, boto3 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_s3_resource():
    """Establish an S3 resource (high-level abstraction of AWS services)"""
    resource = boto3.resource(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),           #specified in .env file in root of project
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")    #specified in .env file in root of project
    )
    return resource

def get_s3_client():
    """Establish an S3 client (lower-level AWS service access)"""
    client = boto3.client(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),           #specified in .env file in root of project
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")    #specified in .env file in root of project
    )
    return client

def generate_trend_line(dataframe, output_path):
    df=dataframe
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    df = df.sort_values('Year')

    x = df['Year']
    y = df['Length_min']

    plt.plot(x, y, 'o')
    plt.plot(x, np.poly1d(np.polyfit(x.dt.year, y, 1))(x.dt.year))

    plt.xlabel('Year')
    plt.ylabel('Length (min)')
    plt.title('Album Lengths Over Time')

    # plt.show()
    plt.savefig(output_path)

if __name__ == '__main__':
    # Load environment variables (AWS access key and secret) from local .env file
    load_dotenv() 

    # Instantiate the s3 object
    s3 = get_s3_client()
    bucket_name = 'jpolkdata-spotify-data'

    # Get the most recent file from s3
    response = s3.list_objects_v2(Bucket=bucket_name)
    sorted_objects = sorted(response['Contents'], key=lambda obj: obj['LastModified'], reverse=True)
    latest_file = sorted_objects[0]
    print(f"==LATEST FILE: {latest_file['Key']}==")

    # Read the contents of the file into a dataframe
    obj = s3.get_object(Bucket=bucket_name, Key=latest_file['Key'])
    df = pd.read_csv(obj["Body"])

    # Calculate the length in minutes and add it to the dataframe
    df['Length_min'] = df['Length_ms'] / 1000 / 60

    # Print the current state of the data
    print(df)

    # Use the data to create a visualization
    generate_trend_line(dataframe=df,output_path='visualizations/album_lengths.png')
    
