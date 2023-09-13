from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import UserProfileModel, MarketCreatedModel


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfileModel.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofilemodel.save()
    

@receiver(pre_save, sender=MarketCreatedModel)
def ensure_single_favorite(sender, instance, **kwargs):
    if instance.favorite:
        # Set all other markets as not favorite
        sender.objects.exclude(pk=instance.pk).update(favorite=False)