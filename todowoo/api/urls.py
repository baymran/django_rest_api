from .views import *
from django.urls import path, include


urlpatterns = [
    path('todos/completed/', TodoCompletedList.as_view())
]