from django.db import models

# Create your models here.
class UserDetails(models.Model):
    name=models.CharField(max_length=255, unique=True)
    email=models.EmailField(max_length=255, unique=True)
    password=models.CharField(max_length=128)
    image=models.ImageField(upload_to='captured_images/',null=True, blank=True)

    def __str__(self):
        return self.email