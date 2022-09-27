from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework import permissions,authentication
from todoapp.models import Todo
from todoapi.serializers import TodoSerializer

# Create your views here.

# class UserRegistrationView(ModelViewSet):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

class TodosView(ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer=TodoSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # def list(self, request, *args, **kwargs):
    #     todos=Todo.objects.filter(user=request.user)
    #     serializer=TodoSerializer(todos,many=True)
    #     return Response(data=serializer.data)


