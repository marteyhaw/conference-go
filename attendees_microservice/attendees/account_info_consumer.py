from datetime import datetime
import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time
import datetime


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "attendees_bc.settings")
django.setup()

from attendees.models import AccountVO


def update_AccountVO(ch, method, properties, body):
    body = json.loads(body)
    first_name = body["first_name"]
    last_name = body["last_name"]
    email = body["email"]
    is_active = body["is_active"]
    updated_string = body["updated"]
    updated = datetime.datetime.fromisoformat(updated_string)
    if is_active:
        print("Account updated or created.")
        print(first_name, last_name, email)
        AccountVO.objects.update_or_create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            updated=updated,
        )
    else:
        account_info = AccountVO.objects.filter(email=email)
        print("Accounts deleted:")
        for i in account_info:
            print(i.first_name, i.last_name, i.email)
        account_info.delete()


while True:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="rabbitmq")
        )
        channel = connection.channel()
        channel.exchange_declare(
            exchange="account_info", exchange_type="fanout"
        )
        result = channel.queue_declare(queue="", exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange="account_info", queue=queue_name)
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=update_AccountVO,
            auto_ack=True,
        )
        channel.start_consuming()
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)

# Based on the reference code at
#   https://github.com/rabbitmq/rabbitmq-tutorials/blob/master/python/receive_logs.py
# infinite loop
#   try
#       create the pika connection parameters
#       create a blocking connection with the parameters
#       open a channel
#       declare a fanout exchange named "account_info"
#       declare a randomly-named queue
#       get the queue name of the randomly-named queue
#       bind the queue to the "account_info" exchange
#       do a basic_consume for the queue name that calls
#           function above
#       tell the channel to start consuming
#   except AMQPConnectionError
#       print that it could not connect to RabbitMQ
#       have it sleep for a couple of seconds
