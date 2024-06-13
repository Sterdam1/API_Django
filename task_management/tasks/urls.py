from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserListCreateView, CurrentUserView,TaskListCreateView, TaskDetailView, TaskCloseView, TaskAssignView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/<int:pk>/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/delete/<int:pk>/', UserListCreateView.as_view(), name='user-delete'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/<int:pk>/assign/', TaskAssignView.as_view(), name='task-assign'),
    path('tasks/<int:pk>/close/', TaskCloseView.as_view(), name='task-close'),
]
