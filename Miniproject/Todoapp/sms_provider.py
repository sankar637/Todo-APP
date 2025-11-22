import os
import logging
import requests

logger = logging.getLogger(__name__)

SMS_PROVIDER = os.environ.get('SMS_PROVIDER', 'textlocal')  # 'textlocal', 'twilio', etc.

def send_sms_textlocal(api_key, numbers, message):
    """
    Textlocal API example (textlocal.in)
    numbers: comma-separated string of numbers or list
    """
    if isinstance(numbers, list):
        numbers = ','.join(numbers)
    url = "https://api.textlocal.in/send/"
    data = {
        'apikey': api_key,
        'numbers': numbers,
        'message': message,
        'sender': os.environ.get('TEXTLOCAL_SENDER', 'TXTLCL')  # set sender if required
    }
    resp = requests.post(url, data=data, timeout=10)
    return resp.json()

def send_sms_twilio(account_sid, auth_token, from_number, to_number, message):
    # Example (uncomment to use Twilio). You must pip install twilio
    # from twilio.rest import Client
    # client = Client(account_sid, auth_token)
    # msg = client.messages.create(body=message, from_=from_number, to=to_number)
    # return {'sid': msg.sid, 'status': msg.status}
    raise NotImplementedError("Twilio function is not enabled in this example.")

def send_sms(phone_number, message):
    """
    Unified function. Reads ENV to pick provider. Returns True if success.
    """
    provider = SMS_PROVIDER.lower()
    try:
        if provider == 'textlocal':
            api_key = os.environ.get('TEXTLOCAL_APIKEY')
            if not api_key:
                logger.warning("TEXTLOCAL_APIKEY not set, SMS not sent. Message: %s", message)
                return False, "No API key"
            res = send_sms_textlocal(api_key, phone_number, message)
            # Textlocal returns 'status' or 'errors' — check response format
            if res.get('status') == 'success' or res.get('status') == 'OK':
                return True, res
            # sometimes response has 'errors' or 'errors' key
            return False, res
        elif provider == 'twilio':
            sid = os.environ.get('TWILIO_ACCOUNT_SID')
            token = os.environ.get('TWILIO_AUTH_TOKEN')
            from_num = os.environ.get('TWILIO_PHONE_NUMBER')
            if not sid or not token or not from_num:
                return False, "Twilio config missing"
            res = send_sms_twilio(sid, token, from_num, phone_number, message)
            return True, res
        else:
            logger.warning("Unknown SMS provider: %s", provider)
            return False, "Unknown provider"
    except Exception as e:
        logger.exception("SMS send error")
        return False, str(e)
