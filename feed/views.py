from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

# Create your views here.

class FeedsView(APIView):
    def get(self, request):
        qs_feeds = Feed.objects.all()
        serializer = FeedDetailSerializer(qs_feeds, many=True)
        return  Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            return  Response(serializer.data, status=status.HTTP_201_CREATED)

