from django.urls import path
from . views import *
urlpatterns = [
    path('', FeedsView.as_view()),
    
]
