import urllib
from questrade_api import Questrade
from dotenv import load_dotenv
from os import getenv
import pandas as pd
import sqlalchemy
import json
import boto3

load_dotenv()

def option_type_mapper(option_type):

    map = {'callSymbolId': 'C', 'putSymbolId': 'P'}

    return map[option_type]

def transform_dataframe(df: pd.DataFrame, stock):

    df = df.optionChain.apply(pd.Series)
    df = df.explode('chainPerRoot', ignore_index=True)
    df = df.drop('chainPerRoot', axis=1).assign(**df.chainPerRoot.apply(pd.Series))
    df = df.explode('chainPerStrikePrice', ignore_index=True)
    df = df.drop('chainPerStrikePrice', axis=1).assign(**df.chainPerStrikePrice.apply(pd.Series))
    df = df.melt(id_vars=['expiryDate','description','listingExchange','optionExerciseType','optionRoot','multiplier','strikePrice'],
                value_vars=['callSymbolId', 'putSymbolId'], var_name='type', value_name='brokerId')
    df['expiryDate'] = pd.to_datetime(df['expiryDate'])
    df['brokerId'] = df['brokerId'].astype(int)
    df['type'] = df['type'].apply(option_type_mapper)
    df['underlyingId'] = stock[0]
    df['greeklyStockId'] = stock[1]

    return df

def insert_option_contracts(questrade: Questrade, stock, engine):
    
    response = json.dumps(questrade.symbol_options(stock[0]))
    df = pd.read_json(response)
    df = transform_dataframe(df, stock)
    df.to_sql('temp_table', engine, if_exists='replace', index=False)

    with engine.begin() as conn, open('transform.sql') as file:

        sql = sqlalchemy.text(file.read())
        conn.execute(sql)

def get_questrade_instance():

    try:
        q = Questrade(token_path=getenv('TOKEN_PATH'))

        time = q.time
        print('time', time)
    except urllib.error.HTTPError as e:
        print('error:', e)
        # s3 = boto3.resource('s3')
        # obj = s3.Object(getenv('AWS_S3_BUCKET'), 'questrade_refresh_token')
        # message = obj.get()['Body'].read().decode('utf-8')
        # token = message.split('=')[1]
        # print(f"TOKEN is {token}")

        # q = Questrade(token_path=getenv('TOKEN_PATH'), refresh_token=token)
    return q

def main():


    greekly_uri = getenv('GREEKLY_DB_URI')
    greekly = sqlalchemy.create_engine(greekly_uri)
    
    # INSERT OPTION CONTRACTS INTO GREEKLY DB
    q = get_questrade_instance()
    sql = 'SELECT broker_id, id FROM stocks'
    stock_list = pd.read_sql(sql=sql, con=greekly_uri).values.tolist()
    
    for stock in stock_list:
        
        insert_option_contracts(q, stock, greekly)

    # PUBLISH OPTION IDS TO SNS
    # sql = 'SELECT broker_id FROM option_contracts WHERE expiration_date > CURRENT_DATE'
    # client = boto3.client('sns', region_name='ca-central-1')
    # arns = json.loads(getenv('COPILOT_SNS_TOPIC_ARNS'))
    # topic_arn = arns.get("broker-option-ids")

    # for chunk in pd.read_sql(sql, con=greekly_uri, chunksize=100):

    #     option_ids = chunk.broker_id.to_list()
    #     client.publish(TopicArn=topic_arn, 
    #                    Message=json.dumps(option_ids))

if __name__ == '__main__':
    
    main()