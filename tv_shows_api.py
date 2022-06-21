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
#Getting most popular tv shows at the moment
url = "https://imdb-api.com/en/API/MostPopularTVs/k_r76n2r9b"
response = requests.get(url)
print(response)
values=json.loads(response.text)
df=pd.DataFrame(values["items"])

#Adding more info to each popular tv show
df2 = pd.DataFrame()

for i in df['id']:
    url = 'https://imdb-api.com/en/API/Title/k_r76n2r9b/' + str(i)
    response = requests.get(url)
    values = json.loads(response.text)
    valuedf = pd.DataFrame([values], columns=values.keys())
    df2 = pd.concat([df2, valuedf], axis =0).reset_index(drop=True)

#Adding current date to file name
current_date = datetime.now().strftime('%Y_%m_%d_%H_%M')
filename = f'tv_show_api_{current_date}.csv'

#Write parsed json data to csv 
df2.to_csv(str(filename), sep=',' ,escapechar='\\', quoting=csv.QUOTE_NONE, encoding='utf-8')

#Send csv to S3 bucket
cli = boto3.client('s3')
s3 = boto3.resource('s3')
filename = str(filename)
bucket = 'team-13-project-data-lake'
key = 'raw-movie-tv-show-data/raw-tv-show-data/' + filename
transfer = S3Transfer(s3_client)

transfer.upload_file(filename, bucket, key)

#Delete CSV file from EC2 instance to save space
os.remove(r'/home/ubuntu/' + filename)