# Generated by Django 4.2.4 on 2023-08-16 02:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article_module', '0012_articlecomments_is_view_by_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='articledislikes',
            name='ip',
            field=models.CharField(default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articlelikes',
            name='ip',
            field=models.CharField(default='127.0.0.1', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='articledislikes',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='articlelikes',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
