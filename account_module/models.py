from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    email_active_code = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='کد فعال سازی')
    phone_number = models.IntegerField(null=True, blank=True, unique=True, verbose_name='شماره تلفن همراه')
    profile_image = models.ImageField(upload_to='images/profile_images', null=True, blank=True, verbose_name='عکس پروفایل')
    is_special_user = models.BooleanField(verbose_name='کاربر ویژه / عادی')
    is_author = models.BooleanField(default=False)
    about_user = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'