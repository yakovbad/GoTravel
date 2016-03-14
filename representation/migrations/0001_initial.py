# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import representation.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, blank=True)),
                ('first_name', models.CharField(max_length=50, blank=True)),
                ('sex', models.CharField(blank=True, max_length=2, choices=[(b'm', b'Male'), (b'fm', b'Female')])),
                ('birthday', models.DateField(null=True, blank=True)),
                ('home_town', models.CharField(max_length=50, blank=True)),
                ('e_mail', models.EmailField(max_length=254, null=True, blank=True)),
                ('mobile_phone', models.CharField(max_length=20, blank=True)),
                ('additional_phone', models.CharField(max_length=100, blank=True)),
                ('personal_site', models.CharField(max_length=255, blank=True)),
                ('activity', models.TextField(blank=True)),
                ('interests', models.TextField(blank=True)),
                ('favorite_music', models.TextField(blank=True)),
                ('favorite_films', models.TextField(blank=True)),
                ('favorite_books', models.TextField(blank=True)),
                ('favorite_games', models.TextField(blank=True)),
                ('user_photo_avatar', models.ImageField(upload_to=representation.models.get_path_user_photo, blank=True)),
                ('city', models.ForeignKey(blank=True, to='representation.City', null=True)),
                ('country', models.ForeignKey(blank=True, to='representation.Country', null=True)),
                ('languages', models.ManyToManyField(to='representation.Language', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(to='representation.Country'),
        ),
    ]
