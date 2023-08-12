# Generated by Django 4.2.4 on 2023-08-10 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('link', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=30)),
                ('copy_right', models.CharField(max_length=200)),
                ('about_site', models.TextField()),
                ('phone_number', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('fax', models.IntegerField()),
                ('address', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LinkBoxes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('links', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='site_module.links')),
            ],
        ),
    ]