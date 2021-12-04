from flask import abort, current_app, request
from functools import wraps
from twilio.request_validator import RequestValidator
import os
import logging

logging.basicConfig(level=logging.INFO)
'''
Note: If your Twilio webhook URLs start with https:// instead of http://, 
your request validator may fail locally when you use Ngrok or in production 
if your stack terminates SSL connections upstream from your app. 
This is because the request URL that your Flask application sees does not
match the URL Twilio used to reach your application.

To fix this for local development with Ngrok, use http:// for your webook 
instead of https://. To fix this in your production app, your decorator 
will need to reconstruct the request's original URL using request headers 
like X-Original-Host and X-Forwarded-Proto, if available.'''


def validate_twilio_request(f):
    """Validates that incoming requests genuinely originated from Twilio"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Create an instance of the RequestValidator class
        validator = RequestValidator(os.environ.get('TWILIO_AUTH_TOKEN'))

        # Validate the request using its URL, POST data,
        # and X-TWILIO-SIGNATURE header
        request_valid = validator.validate(
            request.url,
            request.form,
            request.headers.get('X-TWILIO-SIGNATURE', ''))
        
        twilio_signature = request.headers.get('X-TWILIO-SIGNATURE', '')

        logging.info(f"request url: {request.url}")
        logging.info(f"request form: {request.form}")
        logging.info(f"twilio signature: {twilio_signature}")



        # Continue processing the request if it's valid (or if DEBUG is True)
        # and return a 403 error if it's not
        if request_valid or current_app.debug:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function