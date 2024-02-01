from django.shortcuts import render
from .models import Event
from .serializers import EventSerializer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

event_id_param = openapi.Parameter('event_id', openapi.IN_QUERY, description="Event ID", type=openapi.TYPE_INTEGER)


@swagger_auto_schema(method='get', responses={200: EventSerializer(many=True)})
@swagger_auto_schema(method='post', request_body=EventSerializer)
@api_view(['GET', 'POST'])
def events(request):
    if request.method == "GET":
        events = Event.objects.all()
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

    elif request.method == "PUT":
        pass
    elif request.method == "DELETE":
        pass
    else:
        pass


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
