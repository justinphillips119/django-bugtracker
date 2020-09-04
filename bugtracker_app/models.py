from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    display_name = models.CharField(max_length=50)
    

    def __str__(self):
        return self.username


class Ticket(models.Model):
    NEW = 'New'
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'
    INVALID = 'Invalid'
    COMPLETION_STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
        (INVALID, 'Invalid'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    time_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_by", null=True, blank=True)
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="assigned_to", null=True, blank=True)
    completed_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="completed_by", null=True, blank=True)
    completion_status = models.CharField(max_length=25, choices=COMPLETION_STATUS_CHOICES, default=NEW)

    def __str__(self):
        return self.title
    
