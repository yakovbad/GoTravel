# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-28 09:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('representation', '0005_auto_20160526_0819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_photo_avatar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='album.Photo'),
        ),
    ]
