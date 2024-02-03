import pika
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_to_rabbitmq(queue_name, message):
    credentials = pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, credentials=credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))

    print(" [x] Sent %r" % message)
    connection.close()


def send_event_update(event_id, message):
    channel_layer = get_channel_layer()
    group_name = f'event_{event_id}'

    # Send message to room group
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'event_message',
            'message': message
        }
    )
