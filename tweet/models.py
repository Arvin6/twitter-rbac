import json
import uuid
from enum import Enum

from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.db import models
from tweet.utils import AdminActions, LogActions, LogTypes

class TwitterBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here.
class Tweet(TwitterBase):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    text = models.CharField(max_length=280)
    image_url = models.URLField(null=True)
    likes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    retweets = models.PositiveIntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name="tweet_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="tweet_updated_by")
    
    def delete(self):
        self.is_deleted = True
        self.save()

class RequestAction(TwitterBase):
    action = models.CharField(
        max_length=10, blank=False,
        choices=[(tag.value, tag) for tag in AdminActions]
      )
    tweet_content = models.CharField(max_length=280, blank=True, default='')
    is_approved = models.BooleanField(default=False)
    tweet = models.ForeignKey(Tweet, null=True, on_delete=models.DO_NOTHING, editable=False)
    created_for = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name="tweet_created_for")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name="action_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="action_updated_by")
    
    def approve(self):
        self.is_approved = True
        self.save()

    def save(self):
        if self.is_approved:
            if self.action == AdminActions.create.value:
                # Create a tweet on a user's behalf
                tweet = Tweet(
                        text=self.tweet_content, 
                        created_by=self.created_for, 
                        updated_by=self.created_for
                    )
                tweet.save()
                self.tweet = tweet
            elif self.action == AdminActions.update.value:
                self.tweet.text = self.tweet_content
                self.tweet.updated_by = self.created_for
                self.tweet.save()
            elif self.action == AdminActions.delete.value:
                self.tweet.updated_by = self.created_for
                self.tweet.delete()
        super().save()

class Logs(TwitterBase):
    action = models.CharField(max_length=10, choices=[(tag.value, tag) for tag in LogActions])
    action_type = models.CharField(max_length=10, choices=[(tag.value, tag) for tag in LogTypes])
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    entity = models.CharField(max_length=100)
    resource_id = models.CharField(max_length=100)
