# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import Group


def create_default_groups(apps, schema_editor):
    Group.objects.create(name='user_manager')
    Group.objects.create(name='admin')


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0008_auto_20160904_1905'),
    ]

    operations = [
        migrations.RunPython(create_default_groups),
    ]
