from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from uuid import uuid4

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Friend(models.Model):
    STATUS_TYPE_PENDING = 1
    STATUS_TYPE_ACCEPTED = 2
    STATUS_TYPE_REJECTED = 3
    STATUS_TYPE_CHOICES = (
        (STATUS_TYPE_PENDING, "Pending"),
        (STATUS_TYPE_ACCEPTED, "Accepted"),
        (STATUS_TYPE_REJECTED, "Rejected"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    requester = models.ForeignKey(User, related_name='Requester', on_delete=models.CASCADE)
    requestee = models.ForeignKey(User, related_name='Requestee', on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)
    status_type = models.IntegerField(choices=STATUS_TYPE_CHOICES)

    class Meta:
        unique_together = (
            ("requester", "requestee"),
        )

