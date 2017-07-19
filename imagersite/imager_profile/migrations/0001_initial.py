# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 00:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imager_images.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default='', max_length=25)),
                ('state', models.CharField(default='', max_length=2)),
                ('pic', models.ImageField(upload_to='profile_pics', verbose_name=imager_images.models.ImagerPhoto)),
                ('camera_type', models.CharField(choices=[('CN', 'Canon'), ('NK', 'Nikon'), ('KD', 'Kodak'), ('SN', 'Sony'), ('IP', 'iPhone')], max_length=2)),
                ('photography_style', models.CharField(choices=[('CR', 'Color'), ('BW', 'Black and White'), ('LS', 'Landscape'), ('PR', 'Portrait'), ('MI', 'Micro'), ('MA', 'Macro')], default='CR', max_length=5)),
                ('job', models.CharField(default='', max_length=75)),
                ('website', models.CharField(default='', max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
