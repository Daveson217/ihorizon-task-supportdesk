# Python
from datetime import datetime

# Django
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.
class Request(models.Model):
    summary = models.CharField(max_length=200, blank=False)
    description = models.TextField('Description')
    is_high_priority = models.BooleanField('Flag as high priority', default=False) # Field to check if the Support Ticket is high priority
    is_completed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by') # Customer who submitted the ticket
    user_assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # The agent assigned to the Request
    date_time = models.DateTimeField(auto_now_add=True)
        

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"

    def __str__(self):
        return self.summary
    
    def count_days(self):
        # Method to count how many days ago a Request was created
        today = datetime.now().date()
        date_created = self.date_time.date()
        return (today - date_created).days

    def get_absolute_url(self):
        return reverse("request_detail", kwargs={"pk": self.pk})
