# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import Group


def create_regular_user_role(apps, schema_editor):
    Group.objects.create(name='user')


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0010_auto_20160912_1341'),
    ]

    operations = [
        migrations.RunPython(create_regular_user_role),
    ]
