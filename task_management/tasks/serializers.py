from rest_framework import serializers
from .models import User, Task
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone', 'user_type']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'client', 'employee', 'status', 'created_at', 'updated_at', 'closed_at', 'report']
        read_only_fields = ['created_at', 'updated_at', 'closed_at']

    def validate(self, data):
        if data.get('status') == 'completed' and not data.get('report'):
            raise serializers.ValidationError("Отчет не может быть пустым для выполненной задачи.")
        return data

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description']

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description']

class TaskCloseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['report']
