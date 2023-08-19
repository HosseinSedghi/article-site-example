from django.db import models

from article_module.models import Article


# Create your models here.


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=30)
    copy_right = models.CharField(max_length=200)
    about_site = models.TextField()
    phone_number = models.IntegerField()
    email = models.EmailField()
    fax = models.IntegerField()
    address = models.TextField()

    def __str__(self):
        return self.site_name


class LinkBoxes(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Links(models.Model):
    name = models.CharField(max_length=30)
    link = models.CharField(max_length=200)
    box = models.ForeignKey(LinkBoxes, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Slider(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)