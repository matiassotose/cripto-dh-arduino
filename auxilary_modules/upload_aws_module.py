import boto3
import calendar
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
AWS_ACCESS_KEY_ID = config['AWS']['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = config['AWS']['AWS_SECRET_ACCESS_KEY']

def upload(filename):
    gmt = time.gmtime()
    s3 = boto3.client("s3", aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    s3.upload_file(
        Filename=filename,
        Bucket="cripto-dh-proyect",
        Key=str(calendar.timegm(gmt))+".txt"
    )
