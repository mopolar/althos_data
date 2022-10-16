from email.policy import default
from enum import unique

from django.db import models


class interest_per_region(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False, unique=True)
    first_keyword = models.TextField(blank=False)
    second_keyword = models.TextField(blank=False)
    first_keyword_data = models.TextField(blank=False)
    second_keyword_data = models.TextField(blank=False)


    class Meta:
        ordering = ['created']


class historical(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=False, unique=True)
    keyword = models.TextField(blank=False)
    data = models.JSONField(blank=False)


    class Meta:
        ordering = ['created']