# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='questions/media/'),
        ),
    ]
