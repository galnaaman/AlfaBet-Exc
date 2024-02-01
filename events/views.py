from rest_framework.authtoken.models import Token
from .models import Event
from .serializers import EventSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

event_id_param = openapi.Parameter('event_id', openapi.IN_QUERY, description="Event ID", type=openapi.TYPE_INTEGER)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
    }
), responses={200: openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'token': openapi.Schema(type=openapi.TYPE_STRING, description='Token'),
    }
)})
@api_view(['POST'])
def obtain_auth_token(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid Credentials'}, status=400)


@swagger_auto_schema(method='get',
                     responses={200: EventSerializer(many=True)},
                     manual_parameters=[
                         openapi.Parameter('location', openapi.IN_QUERY, description="Location",
                                           type=openapi.TYPE_STRING),
                         openapi.Parameter('venue', openapi.IN_QUERY, description="Venue", type=openapi.TYPE_STRING),
                         openapi.Parameter('sort_by', openapi.IN_QUERY, description="Sort by", type=openapi.TYPE_STRING,
                                           enum=['date', '-date', 'popularity', '-popularity', 'created', '-created']),
                     ]
                     )
@swagger_auto_schema(method='post', request_body=EventSerializer)
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def events(request):
    if request.method == "GET":
        location = request.query_params.get('location')
        venue = request.query_params.get('venue')
        events = Event.objects.all()
        if location:
            events = events.filter(location__icontains=location)
        if venue:
            events = events.filter(venue__icontains=venue)

        sort_by = request.query_params.get('sort_by')
        if sort_by in ['date', '-date']:
            events = events.order_by('start_time' if sort_by == 'date' else '-start_time')
        elif sort_by in ['popularity', '-popularity']:
            events = events.order_by('popularity' if sort_by == 'popularity' else '-popularity')
        elif sort_by in ['created', '-created']:
            events = events.order_by('creation_time' if sort_by == 'created' else '-creation_time')

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        serializer = EventSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


@swagger_auto_schema(method='get', manual_parameters=[event_id_param], responses={200: EventSerializer(many=False)})
@swagger_auto_schema(method='put', request_body=EventSerializer)
@swagger_auto_schema(method='delete', manual_parameters=[event_id_param])
@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(status=404, data={"message": "Event not found"})

    if request.method == "GET":
        serializer = EventSerializer(event)
        return Response(serializer.data)

    elif request.method == "PUT":
        data = request.data
        serializer = EventSerializer(event, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    elif request.method == "DELETE":
        event.delete()
        return Response(status=204)

@api_view(['GET'])
def event_participants(request):
    pass