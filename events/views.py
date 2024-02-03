from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Event
from .serializers import EventSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_ratelimit.decorators import ratelimit
from django_ratelimit.core import get_usage, is_ratelimited
from django.views.decorators.cache import cache_page

event_id_param = openapi.Parameter('event_id', openapi.IN_QUERY, description="Event ID", type=openapi.TYPE_INTEGER)


@swagger_auto_schema(method='get',
                     responses={200: EventSerializer(many=True)},
                     manual_parameters=[
                         openapi.Parameter('location', openapi.IN_QUERY, description="Location",
                                           type=openapi.TYPE_STRING),
                         openapi.Parameter('venue', openapi.IN_QUERY, description="Venue", type=openapi.TYPE_STRING),
                         openapi.Parameter('sort_by', openapi.IN_QUERY, description="Sort by", type=openapi.TYPE_STRING,
                                           enum=['date', '-date', 'popularity', '-popularity', 'created', '-created']),
                         openapi.Parameter('page', openapi.IN_QUERY, description="Page number",
                                           type=openapi.TYPE_INTEGER)
                     ]
                     )
@swagger_auto_schema(method='post', request_body=EventSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@cache_page(60 * 1)
@ratelimit(key='ip', rate='60/m', block=True)
def events(request):
    if request.method == "GET":
        location = request.query_params.get('location')
        venue = request.query_params.get('venue')
        events_list = Event.objects.all()
        if location:
            events_list = events_list.filter(location__icontains=location)
        if venue:
            events_list = events_list.filter(venue__icontains=venue)

        sort_by = request.query_params.get('sort_by')
        if sort_by in ['date', '-date']:
            events_list = events_list.order_by('start_time' if sort_by == 'date' else '-start_time')
        elif sort_by in ['popularity', '-popularity']:
            events_list = events_list.order_by('popularity' if sort_by == 'popularity' else '-popularity')
        elif sort_by in ['created', '-created']:
            events_list = events_list.order_by('creation_time' if sort_by == 'created' else '-creation_time')

        paginator_events = Paginator(events_list, 1)
        page = request.GET.get('page')
        try:
            page_events = paginator_events.page(page)
        except PageNotAnInteger:
            page_events = paginator_events.page(1)
        except EmptyPage:
            page_events = paginator_events.page(1)

        serializer = EventSerializer(page_events, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        serializer = EventSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


@swagger_auto_schema(method='post', request_body=EventSerializer(many=True))
@swagger_auto_schema(method='put', request_body=EventSerializer(many=True))
@swagger_auto_schema(method='delete', request_body=openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.TYPE_INTEGER))
@api_view(["POST", "PUT", "DELETE"])
def batch_events(request):
    if request.method == "POST":
        data = request.data
        serializer = EventSerializer(data=data, many=True)
        if serializer.is_valid():
            Event.objects.bulk_create([Event(**data) for data in serializer.validated_data])
            return Response({"message": "Events created successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "PUT":
        # Test this route , response should be more intuitive
        data = request.data
        for event_data in data:
            event = get_object_or_404(Event, id=event_data.get('id'))
            serializer = EventSerializer(event, data=event_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Events updated successfully"}, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        # if fail to delete any event, it should return a message with what events already deleted
        data = request.data
        for event_id in data:
            event = get_object_or_404(Event, id=event_id)
            try:
                event.delete()
            except Exception as e:
                pass
        return Response({"message": "Events deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


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


@swagger_auto_schema(method='post',
                     manual_parameters=[event_id_param],
                     request_body=openapi.Schema(
                         type=openapi.TYPE_OBJECT,
                         properties={
                             'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                         }))
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_to_event(request, event_id):
    print(request.body)
    event = get_object_or_404(Event, id=event_id)
    user = get_object_or_404(User, id=request.data.get('user_id'))
    # Check if the user is already subscribed
    if user in event.participants.all():
        return Response({'message': 'You are already subscribed to this event.'}, status=400)
    event.participants.add(user)
    event.popularity = event.popularity_count
    event.save()
    return Response({'message': 'Successfully subscribed to the event.'})
