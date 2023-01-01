from rest_framework.parsers import JSONParser
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
from django.db import IntegrityError
from todo.models import Todo
from .serializers import TodoSerializer, TodoCompleteSerializer


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(username=data['username'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            response = {'token': str(token)}
            return JsonResponse(response, status=201)
        except IntegrityError:
            response = {'error': 'That username has already been taken. Please choose another name.'}
            return JsonResponse(response, status=400)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None:
            response = {'error': 'Could not login. Please check username and password.'}
            return JsonResponse(response, status=200)
        else:
            try:
                token = Token.objects.get(user=user)
                response = {'token': str(token)}
            except:
                token = Token.objects.create(user=user)
                response = {'token': str(token)}
            return JsonResponse(response, status=200)


class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        objects = Todo.objects.filter(user=user, datecompleted__isnull=False).order_by('-datecompleted')
        return objects


class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        objects = Todo.objects.filter(user=user, datecompleted__isnull=True)
        return objects

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        objects = Todo.objects.filter(user=user)
        return objects


class TodoComplete(generics.RetrieveUpdateAPIView):
    serializer_class = TodoCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.datecompleted = timezone.now()
        serializer.save()










