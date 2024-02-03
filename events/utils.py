from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

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
