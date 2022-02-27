from os import getenv
from flask import request, jsonify, Blueprint
from .serializers import OptionContractsSchema, StocksSchema
from .models import OptionContracts, Stocks, Users
from .exceptions import GreeklyException
from .decorators import validate_twilio_request
from sqlalchemy.exc import IntegrityError
from twilio.twiml.messaging_response import MessagingResponse
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from . import db
import boto3
import json
from datetime import datetime


bp = Blueprint('app_bp', __name__)


@bp.errorhandler(GreeklyException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@bp.route('/sms', methods=['POST'])
@validate_twilio_request
def sms_reply():

    body = request.values.get('Body', None)
    """Respond to incoming calls with a simple text message."""

    # Start our TwiML response
    resp = MessagingResponse()

    # publish message to SNS
    try: 
        client = boto3.client('sns', region_name='ca-central-1')

        arns = json.loads(getenv('COPILOT_SNS_TOPIC_ARNS'))

        topic_arn = arns.get("greekly-api-2fa-codes")

        client.publish(TopicArn=topic_arn, 
                Message=json.dumps({"body": body}))
        
        resp.message(f"Published to SNS: {body}")
    except:
        
        resp.message(f"Failed to publish to SNS: {body}")

    return str(resp)


@bp.route('/', methods=['GET'])
def healthcheck():
    return "Health is good!"

@bp.route('/stocks', methods=['GET', 'POST'])
@jwt_required()
def stocks():

    if request.method == 'GET':

        if len(request.args) > 1:
            raise GreeklyException("Please specify only one of ['ticker', 'id', 'description', 'exchange', 'broker_id']")
        
        ticker = request.args.get('ticker')
        if ticker:
            res = Stocks.query.filter_by(ticker=ticker).first()
            return StocksSchema().dump(res)

        stock_id = request.args.get('id')
        if stock_id:
            res = Stocks.query.filter_by(id=stock_id).first()
            return StocksSchema().dump(res)

        description = request.args.get('description')
        if description:
            res = Stocks.query.filter_by(description=description).first()
            return StocksSchema().dump(res)
        
        res = Stocks.query.all()
        
        return jsonify(StocksSchema(many=True).dump(res))
    
    if request.method == 'POST':

        if not request.json:
            raise GreeklyException("No input provided")
        
        request_obj = request.get_json()
        
        if not 'ticker' in request_obj:
            raise GreeklyException("Ticker is required")
        
        if not 'description' in request_obj:
            raise GreeklyException("Company description is required")

        if not 'broker_id' in request_obj:
            raise GreeklyException("Broker stock ID is required")

        if not 'exchange' in request_obj:
            raise GreeklyException("Exchange is required")

        stock = Stocks(ticker=request_obj['ticker'],
                       description=request_obj['description'],
                       broker_id=request_obj['broker_id'],
                       exchange=request_obj['exchange'],)

        db.session.add(stock)
        db.session.commit()

        return StocksSchema().dump(Stocks.query.filter_by(ticker=request_obj['ticker']).first())

@bp.route('/option_contracts', methods=['GET'])
@jwt_required()
def option_contracts():

    res = OptionContracts.query

    page = request.args.get('page', 1, type=int)

    type = request.args.get('type')
    if type:
        res = res.filter_by(type = type)
    
    max_delta = request.args.get('max_delta')
    if max_delta:
        res = res.filter(OptionContracts.delta <= float(max_delta))

    min_delta = request.args.get('min_delta')
    if min_delta:
        res = res.filter(OptionContracts.delta >= float(min_delta))

    max_theta = request.args.get('max_theta')
    if max_theta:
        res = res.filter(OptionContracts.theta <= float(max_theta))

    min_theta = request.args.get('min_theta')
    if min_theta:
        res = res.filter(OptionContracts.theta >= float(min_theta))

    max_gamma = request.args.get('max_gamma')
    if max_gamma:
        res = res.filter(OptionContracts.gamma <= float(max_gamma))

    min_gamma = request.args.get('min_gamma')
    if min_gamma:
        res = res.filter(OptionContracts.gamma >= float(min_gamma))
    
    max_rho = request.args.get('max_rho')
    if max_rho:
        res = res.filter(OptionContracts.rho <= float(max_rho))

    min_rho = request.args.get('min_rho')
    if min_rho:
        res = res.filter(OptionContracts.rho >= float(min_rho))
    
    max_vega = request.args.get('max_vega')
    if max_vega:
        res = res.filter(OptionContracts.vega <= float(max_vega))

    min_vega = request.args.get('min_vega')
    if min_vega:
        res = res.filter(OptionContracts.vega >= float(min_vega))

    max_strike = request.args.get('max_strike')
    if max_strike:
        res = res.filter(OptionContracts.strike_price <= float(max_strike))

    min_strike = request.args.get('min_strike')
    if min_strike:
        res = res.filter(OptionContracts.strike_price >= float(min_strike))

    max_expiration = request.args.get('max_expiration')
    if max_expiration:
        res = res.filter(OptionContracts.expiration_date <= datetime.strptime(max_expiration, '%Y-%m-%d'))
    
    min_expiration = request.args.get('min_expiration')
    if min_expiration:
        res = res.filter(OptionContracts.expiration_date >= datetime.strptime(min_expiration, '%Y-%m-%d'))
    
    max_volatility = request.args.get('max_volatility')
    if max_volatility:
        res = res.filter(OptionContracts.volatility <= float(max_volatility))

    min_volatility = request.args.get('min_volatility')
    if min_volatility:
        res = res.filter(OptionContracts.volatility >= float(min_volatility))

    max_bid_price = request.args.get('max_bid_price')
    if max_bid_price:
        res = res.filter(OptionContracts.bid_price <= float(max_bid_price))

    min_bid_price = request.args.get('min_bid_price')
    if min_bid_price:
        res = res.filter(OptionContracts.bid_price >= float(min_bid_price))

    max_ask_price = request.args.get('max_ask_price')
    if max_ask_price:
        res = res.filter(OptionContracts.ask_price <= float(max_ask_price))

    min_ask_price = request.args.get('min_ask_price')
    if min_ask_price:
        res = res.filter(OptionContracts.ask_price >= float(min_ask_price))
    
    response = res.paginate(page, 10, False)

    res_serialized = OptionContractsSchema().dump(response.items, many=True)

    data = {
        'total_pages': response.pages,
        'current_page': response.page,
        'total_items': response.total,
        'items': res_serialized
    }

    return jsonify(data)

# @bp.route('/register', methods=['POST'])
# def register():

#     try:
#         email = request.json.get('email', None)
#         password = request.json.get('password', None)
        
#         if not email: raise GreeklyException("Email is required", status_code=400)
#         if not password: raise GreeklyException("Password is required", status_code=400)
        
#         hashed = generate_password_hash(password)

#         user = Users(email=email, password_hash=hashed)
#         db.session.add(user)
#         db.session.commit()

#         access_token = create_access_token(identity={"email": email})
#         return {"access_token": access_token}, 200
#     except IntegrityError:
#         db.session.rollback()
#         raise GreeklyException("User already exists", status_code=400)

@bp.route('/login', methods=['POST'])
def login():

    email = request.json.get('email', None)
    password = request.json.get('password', None)
    
    if not email:
        raise GreeklyException("Email is missing", status_code=400)
    if not password:
        raise GreeklyException("Password is missing", status_code=400)
    
    user = Users.query.filter_by(email=email).first()
    if not user:
        raise GreeklyException("User not found", status_code=404)

    if not user.check_password(password):
        raise GreeklyException("Invalid password", status_code=401)
    
    if not user.is_approved:
        raise GreeklyException("User is not approved to make requests", status_code=401)
    
    access_token = create_access_token(identity={"email": email})
    return {"access_token": access_token}, 200

