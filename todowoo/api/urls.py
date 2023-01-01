from .views import *
from django.urls import path, include


urlpatterns = [
    path('todos/', TodoListCreate.as_view()),
    path('todos/<int:pk>/', TodoRetrieveUpdateDestroy.as_view()),
    path('todos/<int:pk>/complete/', TodoComplete.as_view()),
    path('todos/completed/', TodoCompletedList.as_view()),
    # AUTH
    path('signup/', signup),
    path('login/', login)
]