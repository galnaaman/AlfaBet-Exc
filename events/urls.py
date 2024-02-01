from django.urls import path
from .views import *

urlpatterns = [
    path("events/", events, name="events-list-create"),
    path("events/<int:event_id>", event_detail, name="event-detail"),
    path('token/', obtain_auth_token, name='api-token'),

]
