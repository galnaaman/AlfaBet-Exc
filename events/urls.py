from django.urls import path
from events.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path("events/", events, name="events-list-create"),
    path("events/batch/", batch_events, name="batch-events"),
    path("events/<int:event_id>", event_detail, name="event-detail"),
    path("events/<int:event_id>/subscribe/", subscribe_to_event, name="subscribe_to_event"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),


]
