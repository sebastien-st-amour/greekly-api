from dotenv import load_dotenv
from os import getenv, getcwd, path, remove
from classes import *
import boto3

load_dotenv()
username = getenv('QUESTRADE_USERNAME')
password = getenv('QUESTRADE_PASSWORD')

sqs = SQSListener(getenv('AWS_SQS_QUEUE_URI'))

session = QuestradeSession(sqs_client=sqs, chrome_url=getenv('CHROME_URL'))

api_token = session.get_api_token(username, password)

path_to_file = path.join(getcwd(), "questrade_refresh_token")

f = open(path_to_file, "w")
f.write(f"TOKEN={api_token}")
f.close()

resource = boto3.resource('s3')
resource.meta.client.upload_file(path_to_file, getenv('AWS_S3_BUCKET'), "questrade_refresh_token")

remove(path_to_file)

print('API Token: ', api_token)