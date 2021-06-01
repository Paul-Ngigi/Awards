from django.db import models
from pyuploadcare.dj.models import ImageField, FileField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from cloudinary.models import CloudinaryField


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='profile')
    dp = ImageField(manual_crop='1024x1024')
    bio = HTMLField(max_length=500)
    phone_number = models.BigIntegerField()

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    def __str__(self):
        return self.user.username
