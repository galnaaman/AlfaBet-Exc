# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from events import consumers

websocket_urlpatterns = [
    path('ws/events/<int:event_id>/', consumers.EventConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
