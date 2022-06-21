#import all needed modules
import requests
import json
import pandas as pd
import csv
from datetime import datetime
import boto3
from boto3.s3.transfer import S3Transfer
import os

s3_client = boto3.client(service_name='s3', region_name='us-east-1',
                         aws_access_key_id='AKIAWPWIFLV3Z3DONRYF',
                         aws_secret_access_key='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')

#Import json data from API
url = "http://api.aviationstack.com/v1/flights"
params = {
    'access_key': '522c8f6e08837b3734f8c2bcfb1fcab0',
    'flight_status': 'scheduled',
    'flight_date': datetime.today().strftime('%Y-%m-%d')
}
response = requests.get(url, params)
print(response)
df=json.loads(response.text)
df2=pd.DataFrame(df["data"])

# Adding current date to file name
current_date = datetime.now().strftime('%Y_%m_%d_%H_%M')
filename = f'flight_api_{current_date}.csv'

#Write parsed json data to csv 
df2.to_csv(str(filename), sep=',' ,escapechar='\\', quoting=csv.QUOTE_NONE, encoding='utf-8')

#Send csv to S3 bucket
cli = boto3.client('s3')
s3 = boto3.resource('s3')
filename = str(filename)
bucket = 'team-13-project-data-lake'
key = 'raw-flights-data/' + filename
transfer = S3Transfer(s3_client)

transfer.upload_file(filename, bucket, key)

#Delete CSV file from EC2 instance to save space
os.remove(r'/home/ubuntu/' + filename)