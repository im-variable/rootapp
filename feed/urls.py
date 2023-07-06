from django.urls import path
from . views import *
urlpatterns = [
    path('', FeedListView.as_view()),
    path('<pk>/', FeedDetailView.as_view()),
    
]
