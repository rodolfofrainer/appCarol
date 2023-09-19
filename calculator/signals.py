from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    from .models import UserProfileModel
    if created:
        UserProfileModel.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    from .models import UserProfileModel
    instance.userprofilemodel.save()

@receiver(pre_save, sender='calculator.MarketCreatedModel')
def ensure_single_favorite(sender, instance, **kwargs):
    from .models import MarketCreatedModel
    if instance.favorite:
        sender.objects.filter(user_id=instance.user_id).exclude(
            pk=instance.pk).update(favorite=False)