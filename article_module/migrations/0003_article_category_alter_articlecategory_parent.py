# Generated by Django 4.2.4 on 2023-08-10 10:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0002_alter_articlecategory_parent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(related_name='category', to='article_module.articlecategory'),
        ),
        migrations.AlterField(
            model_name='articlecategory',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='article_module.articlecategory'),
        ),
    ]