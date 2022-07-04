import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def sendsms():

    account_sid = "ACd315812105d4be30d3a94b54aa787b63"
    auth_token = "4550ed9b1667036fcc7869c3f7d96b0e"
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="Your One Time Password is:",
                        from_='+19783203127',
                        to='+918086374853'
                    )
    print('Message sent successfully.')
