from django.contrib.auth.models import User
from rest_framework import serializers
from todoapp.models import Todo


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             "username",
#             "password",
#             "email"
#         ]
#
#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)


class TodoSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    class Meta:
        model = Todo
        fields = "__all__"

    def create(self, validated_data):
        user=self.context.get("user")
        return Todo.objects.create(**validated_data,user=user)