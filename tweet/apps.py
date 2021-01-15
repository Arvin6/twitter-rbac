from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver

class TweetConfig(AppConfig):
    name = 'tweet'

    def ready(self):
        from tweet.signals import log_action, log_tweet
