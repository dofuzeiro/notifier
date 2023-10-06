import subprocess
import sys
import datetime
import os
from twilio.rest import Client

urls = os.getenv('URL')
colors = os.getenv('COLORS')
bike_size = os.getenv('SIZE')
to = os.getenv('TO')
from_ = os.getenv('FROM')
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
send_notification = os.getenv('SEND_NOTIFICATION')

if urls is None:
    raise Exception('URL must be specified')
if colors is None:
    raise Exception('Color must be specified')
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
if send_notification is None:
    raise Exception('Send notification must be specified')

colors = colors.split(',')

for index, url in urls.split(','):
    
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

        if 'brevemente' not in output and send_notification.upper() == 'S':
            message = client.messages.create(
                to=to,
                from_=from_,
                body=f'Bicicleta disponível, cor: {colors[index]}, tamanho: {bike_size}, através do url: {url}'
            )

        with open('results.log', 'a') as file:
            file.write(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: cor: {colors[index]}, {output}")

    except Exception as e:
        raise Exception(f"Error while executing the script: {e}")
