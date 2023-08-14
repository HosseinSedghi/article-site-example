from django.db import models
from django.utils import timezone

from account_module.models import User


# Create your models here.

class ArticleCategory(models.Model):
    parent = models.ForeignKey('ArticleCategory', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    title = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(max_length=250, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    STATUS = (
        ('publish', 'انتشار'),
        ('draft', 'پیش نویس'),
        ('lock', 'در حال برسی ...'),
        ('back', 'برگشت داده شده')
    )
    title = models.CharField(max_length=50, unique=True, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True)
    image = models.ImageField(upload_to='images/article_images')
    category = models.ManyToManyField(ArticleCategory, related_name='category')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    is_special = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS, default='draft', max_length=20)
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True, null=True, blank=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    is_update = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.title


class ArticleComments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    is_publish = models.BooleanField(default=False)
    replay = models.ForeignKey('ArticleComments', on_delete=models.CASCADE, related_name='comment_replay', null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} / {self.article}"


class ArticleView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.CharField(max_length=30, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.ip


class ArticleLikes(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ArticleDisLikes(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)