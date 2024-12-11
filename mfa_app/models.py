from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets

class UserDetails(models.Model):
    name=models.CharField(max_length=255, unique=True)
    email=models.EmailField(max_length=255, unique=True)
    password=models.CharField(max_length=128)
    image=models.ImageField(upload_to='captured_images/',null=True, blank=True)
    token=models.CharField(max_length=64, unique=True, blank=True)
    def __str__(self):
        return self.email
    
@receiver(post_save, sender=UserDetails)
def _post_save_receiver(sender, instance, created, **kwargs):
    if created and not instance.token:
        instance.token = secrets.token_hex(32)  # Generates a 64-character hexadecimal token
        instance.save()