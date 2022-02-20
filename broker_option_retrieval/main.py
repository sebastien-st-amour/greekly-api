
from questrade_api import Questrade
from os import getenv
import urllib
import logging
import json
import boto3

class SQSListener:
    
    def __init__(self, queue_url):

        self.queue_url = queue_url
        arns = json.loads(getenv('COPILOT_SNS_TOPIC_ARNS'))
        self.topic_arn = arns.get("broker-option-responses")
        self.sqs = boto3.client('sqs')
        self.sns = boto3.client('sns')
        self.s3 = boto3.resource('s3')
        self.questrade = Questrade(token_path=getenv('TOKEN_PATH'))
        logging.basicConfig(level=logging.INFO)
    
    def __poll(self):
        
        response = self.sqs.receive_message(QueueUrl = self.queue_url,
                                               MaxNumberOfMessages = 1,
                                               WaitTimeSeconds = 20)
        
        if 'Messages' in response:

            logging.info("Message received")

            return self.__handle_response(response)
        else:
            return None
    
    def __handle_response(self, response):

        message = response['Messages'][0]
        self.__delete(message['ReceiptHandle'])
        body = json.loads(message['Body'])
        content = json.loads(body['Message'])
        
        logging.info(f"Message body is {content}")

        self.publish_options_data_to_sns(content)

    def __delete(self, receipt_handle):
        
        self.sqs.delete_message(QueueUrl = self.queue_url,
                                   ReceiptHandle = receipt_handle)

    def publish_options_data_to_sns(self, option_ids):

        questrade_options_data = self.fetch_market_data_for_option_ids(option_ids)
        
        if not questrade_options_data:
            logging.info("No data to publish")
            return
        self.sns.publish(TopicArn = self.topic_arn,
                         Message = json.dumps(questrade_options_data))

    def fetch_market_data_for_option_ids(self, option_ids):
        
        try:
            
            return self.questrade.markets_options(optionIds=option_ids)
        
        except urllib.error.HTTPError as e:

            logging.error(e)

        try:
            
            # re-authenticate
            self.questrade = Questrade(token_path=getenv('TOKEN_PATH'))

            return self.questrade.markets_options(optionIds=option_ids)
        
        except urllib.error.HTTPError as e:

            logging.error(e)

            token = self._get_new_refresh_token()
            
            self.questrade = Questrade(refresh_token=token, token_path=getenv('TOKEN_PATH'))
            
            return self.questrade.markets_options(optionIds=option_ids)
    
    def _get_new_refresh_token(self):

        logging.info("Fetching refresh token from S3 bucket")
        
        obj = self.s3.Object(getenv('BROKEROPTIONRETRIEVAL_NAME'), 'questrade_refresh_token')
        
        message = obj.get()['Body'].read().decode('utf-8')
        token = message.split('=')[1]

        logging.info(f"TOKEN is {token}")

        return token


    def listen(self):
    
        while True: self.__poll()

listener = SQSListener(getenv('COPILOT_QUEUE_URI'))
listener.listen()