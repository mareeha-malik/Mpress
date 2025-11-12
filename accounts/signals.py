from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import utils as db_utils
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except (db_utils.OperationalError, db_utils.ProgrammingError):
            # DB isn't ready (migrations not applied) — skip creating profile now
            return


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        # Attempt to save linked profile if it exists
        instance.profile.save()
    except Profile.DoesNotExist:
        try:
            Profile.objects.create(user=instance)
        except (db_utils.OperationalError, db_utils.ProgrammingError):
            # Database/table isn't ready yet; ignore to avoid crashing during migrations
            return
    except (db_utils.OperationalError, db_utils.ProgrammingError):
        # Database not ready (no table yet). Avoid raising and let migrations run.
        return
