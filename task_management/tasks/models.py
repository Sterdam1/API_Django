from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employee', 'Employee'),
        ('client', 'Client'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает исполнителя'),
        ('in_progress', 'В процессе'),
        ('completed', 'Выполнена'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    client = models.ForeignKey(User, related_name='created_tasks', on_delete=models.CASCADE, limit_choices_to={'user_type': 'client'})
    employee = models.ForeignKey(User, related_name='assigned_tasks', null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'user_type': 'employee'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    report = models.TextField(blank=True)

    def assign_to_employee(self, employee):
        self.employee = employee
        self.status = 'in_progress'
        self.save()

    def close_task(self, report):
        self.status = 'completed'
        self.report = report
        self.closed_at = datetime.now()
        self.save()