import subprocess
import sys
import datetime
import os
from twilio.rest import Client


url = os.getenv('URL')
bike_size = os.getenv('SIZE')
to = os.getenv('SIZE')
from_ = os.getenv('SIZE')
account_sid = os.getenv('SIZE')
auth_token = os.getenv('SIZE')

if url is None:
    raise Exception('URL must be specified')
if bike_size is None:
    raise Exception('Bike size must be specified')
if to is None:
    raise Exception('To must be specified')
if from_ is None:
    raise Exception('From must be specified')
if account_sid is None:
    raise Exception('Account_sid must be specified')
if auth_token is None:
    raise Exception('Auth_token must be specified')


command = [
    "curl", "-s", url,
    "|",
    "grep", "-i", "-A", "7", f"\"data-product-size=\\\"{bike_size}\\\"\"",
    "|",
    "tail", "-n", "1"
]


try:
    result = subprocess.run(" ".join(command), check=True, capture_output=True, shell=True)
    output = result.stdout.decode('utf-8')
    client = Client(account_sid, auth_token)

    if 'brevemente' not in output:
        print('entrei')
        message = client.messages.create(
            to=to,
            from_=from_,
            body=f'Bicicleta disponível tamanho: {bike_size} através do url: {url}'
        )
    
except Exception as e:
    raise Exception(f"Error while executing the script: {e}")
