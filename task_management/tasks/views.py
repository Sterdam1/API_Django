from rest_framework import generics, permissions, status, serializers
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer, TaskCreateSerializer, TaskUpdateSerializer, TaskCloseSerializer
from .permissions import IsEmployeeOrReadOnly, IsTaskOwnerOrEmployee, IsClient, IsAdmin

class CurrentUserView(generics.ListCreateAPIView): 
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        serializer_class = UserSerializer(request.user)
        return Response(serializer_class.data)

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        refresh = RefreshToken.for_user(user)

        response_data = serializer.data
        response_data['refresh'] = str(refresh)
        response_data['access'] = str(refresh.access_token)

        return Response(response_data, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsEmployeeOrReadOnly()]
        elif self.request.method == 'GET':
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.IsAuthenticated()]
    
    def get_object(self):
        user_id = self.kwargs['pk']
        return get_object_or_404(User, pk=user_id)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            user.is_active = True
            user.is_authenticated = True
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = get_object_or_404(User, pk=user_id)
        
        if not request.user.is_superuser:
            return Response({"detail": "Только администратор может удалять пользователей."}, status=status.HTTP_403_FORBIDDEN)
        
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'employee' or user.is_superuser:
            return Task.objects.all()
        return Task.objects.filter(client=user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

class TaskDetailView(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsTaskOwnerOrEmployee]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TaskUpdateSerializer
        return TaskSerializer

    def perform_update(self, serializer):
        task = serializer.instance
        if task.status == 'completed':
            raise serializers.ValidationError("Завершенную задачу редактировать нельзя.")
        serializer.save()

class TaskAssignView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTaskOwnerOrEmployee]

    def post(self, request, pk, format=None):
        task = get_object_or_404(Task, pk=pk)
        if task.status != 'pending':
            return Response({"detail": "Эта задача уже была назначена."}, status=status.HTTP_400_BAD_REQUEST)
        task.assign_to_employee(request.user)
        return Response(TaskSerializer(task).data)

class TaskCloseView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsTaskOwnerOrEmployee]

    def post(self, request, pk, format=None):
        task = get_object_or_404(Task, pk=pk)
        if task.status != 'in_progress':
            return Response({"detail": "Только задачи в процессе могут быть закрыты."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TaskCloseSerializer(data=request.data)
        if serializer.is_valid():
            task.close_task(serializer.validated_data['report'])
            return Response(TaskSerializer(task).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)