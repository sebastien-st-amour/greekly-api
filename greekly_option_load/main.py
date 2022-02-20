
import os
import logging
import sqlalchemy
import pandas as pd
import json
import boto3

class SQSListener:
    
    def __init__(self, queue_url):

        self.queue_url = queue_url
        self.sqs = boto3.client('sqs')
        self.greekly_engine = sqlalchemy.create_engine(os.getenv('GREEKLY_DB_URI'))
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
        
        self.load_options_data_to_greekly_db(body['Message'])
        self.execute_sql_transformation()

    def __delete(self, receipt_handle):
        
        self.sqs.delete_message(QueueUrl = self.queue_url,
                                   ReceiptHandle = receipt_handle)

    def load_options_data_to_greekly_db(self, options):

        try:
            df = self.generate_dataframe(options)
            
            with self.greekly_engine.connect() as connection:

                connection.detach()
                
                with connection.begin():
                    
                    df.to_sql('temp_option_details', con=connection, if_exists='replace', index=False)

        except Exception as e:
            
            logging.error(e)
            pass

    def generate_dataframe(self, option_data: str):

        logging.info("Generating dataframe")
        logging.info(option_data)

        df = pd.read_json(option_data)
        df = df.drop('optionQuotes', axis=1).assign(**df.optionQuotes.apply(pd.Series))
        df['lastTradeTime'] = pd.to_datetime(df['lastTradeTime'])
        df['bidPrice'] = df['bidPrice'].fillna(0)
        df['askPrice'] = df['askPrice'].fillna(0)
        df['lastTradePriceTrHrs'] = df['lastTradePriceTrHrs'].fillna(0)
        df['lastTradePrice'] = df['lastTradePrice'].fillna(0)

        return df
    
    def execute_sql_transformation(self):
    
        with self.greekly_engine.connect() as conn, open('transform.sql') as file:
            
            sql = sqlalchemy.text(file.read())

            conn.detach()

            with conn.begin():
                
                conn.execute(sql)
    
    def listen(self):
    
        while True: self.__poll()

listener = SQSListener(os.getenv('COPILOT_QUEUE_URI'))
listener.listen()