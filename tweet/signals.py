import logging
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver

from tweet.models import Logs, Tweet, RequestAction
from tweet.utils import AdminActions, LogTypes, LogActions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(process)d %(thread)d - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

@receiver(post_save, sender=RequestAction)
def log_action(sender, instance, created, *args, **kwargs):
    logger.info("Received signal from %s", sender)
    if created:
        action = LogActions.create.value
        action_type = LogTypes.action
    elif (instance.is_approved and not created):
        action = LogActions.update.value
        action_type = LogTypes.audit
    else:
        action = instance.action
        action_type = LogTypes.action
    log_instance = Logs(
        action=action,
        action_type=action_type.value,
        user=instance.updated_by,
        entity=sender.__name__,
        resource_id=instance.id
    )
    log_instance.save()

@receiver(post_save, sender=Tweet)    
def log_tweet(sender, instance, created, *args, **kwargs):
    logger.info("Received signal from %s", sender)
    if created:
        action = LogActions.create.value
        action_type = LogTypes.action
    elif instance.is_deleted:
        action = LogActions.delete.value
        action_type = LogTypes.audit
    else:
        action = LogActions.update.value
        action_type = LogTypes.action
    log_instance = Logs(
        action=action,
        action_type=action_type.value,
        user=instance.updated_by,
        entity=sender.__name__,
        resource_id=instance.id
    )
    log_instance.save()

@receiver(user_logged_in)
def post_login(sender, user, *args, **kwargs):
    logger.info("User login signal received")
    log_instance = Logs(
        action=LogActions.login.value,
        action_type=LogTypes.access.value,
        user=user,
        entity=sender.__name__,
        resource_id=user.id
    )
    log_instance.save()
