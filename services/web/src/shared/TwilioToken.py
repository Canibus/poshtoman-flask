from flask import json, request, Response, current_app
from twilio.rest import Client, TwilioException
from functools import wraps
from ..models.ClientModel import ClientModel

class Token:
    @staticmethod
    def _get_twilio_verify_client():
        return Client(
        current_app.config['TWILIO_ACCOUNT_SID'],
        current_app.config['TWILIO_AUTH_TOKEN']).verify.services(
            current_app.config['TWILIO_VERIFY_SERVICE_ID'])

    @staticmethod
    def request_verification_token(phone):
        verify = Token._get_twilio_verify_client()
        verify.verifications.create(to=phone, channel='sms')

    @staticmethod
    def check_verification_token(phone, token):
        verify = Token._get_twilio_verify_client()
        try:
            result = verify.verification_checks.create(to=phone, code=token)
        except TwilioException:
            return False
        return result.status == 'approved'
