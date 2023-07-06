from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *

# Create your views here.

class FeedListView(APIView):
    def get(self, request):
        qs_feeds = Feed.objects.all()
        serializer = FeedDetailSerializer(qs_feeds, many=True)
        context = {'data': serializer.data, 'message': 'Data fetched successfully'}
        return  Response(context , status=status.HTTP_200_OK)

    def post(self, request):
        serializer = FeedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            context = {'data': serializer.data, 'message': 'Data saved successfully'}
            return Response(context , status=status.HTTP_201_CREATED)
        
        context = {'message': serializer.errors}
        return Response(context , status=status.HTTP_400_BAD_REQUEST)


class FeedDetailView(APIView):
    
    def get_queryset(self, pk):
        qs = Feed.objects.get(id=pk)
        return qs
    
    def get(self, request, pk, **kwargs):
        feed_obj = self.get_queryset(pk)
        serializer = FeedDetailSerializer(feed_obj)
        context = {'data': serializer.data , "message": "feed detail fetched successfully"}
        return Response(context , status=status.HTTP_200_OK)


    def put(self, request, pk, **kwargs):
        feed_obj = self.get_queryset(pk)
        serializer = FeedSerializer(feed_obj, data=request.data, context={'user': 1})
        if serializer.is_valid():
            serializer.save()
            context = {'data': serializer.data , "message": "feed detail fetched successfully"}
            return Response(context , status=status.HTTP_200_OK)
        
        context = {'message': serializer.errors}
        return Response(context , status=status.HTTP_400_BAD_REQUEST)
