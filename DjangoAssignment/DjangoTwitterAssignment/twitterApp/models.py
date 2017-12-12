from django.db import models

# Create your models here.
# MODELS to SAVE TWITER HANDLE,TWEETS AND DATE
class DatewiseTweets(models.Model):
    name = models.CharField(max_length=140)
    tweets = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True)
