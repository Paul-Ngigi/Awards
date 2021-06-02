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


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=5000, null=True)
    link = models.URLField()
    image1 = ImageField(manual_crop='1024x1024')
    image2 = ImageField(manual_crop='1024x1024')
    image3 = ImageField(manual_crop='1024x1024')
    postedon = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-id']

    @classmethod
    def save_post(self):
        self.save()

    @classmethod
    def get_posts(cls):
        posts = cls.objects.all()
        return posts

    @classmethod
    def delete_post(self):
        self.delete()

    @classmethod
    def delete_image_by_id(cls, id):
        post = cls.objects.filter(pk=id)
        post.delete()

    @classmethod
    def get_image_by_id(cls, id):
        post = cls.objects.get(pk=id)
        return post


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE,
                             related_name='comments')
    comment = models.CharField(max_length=2000)
    posted_on = models.DateTimeField(auto_now_add=True)

    @classmethod
    def save_comment(self):
        self.save()

    @classmethod
    def get_comment(cls):
        posts = cls.objects.all()
        return posts

    @classmethod
    def delete_comment(self):
        self.delete()

    @classmethod
    def delete_comment_by_id(cls, id):
        comment = cls.objects.filter(pk=id)
        comment.delete()

    @classmethod
    def get_comment_by_id(cls, id):
        comment = cls.objects.get(pk=id)
        return comment


RATE_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), ]


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='likes')
    creativity = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)
    content = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)
    design = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)
    usability = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return self.user.username
