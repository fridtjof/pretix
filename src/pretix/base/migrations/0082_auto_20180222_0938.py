# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-22 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pretixbase', '0081_auto_20180220_1031'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='checkin_attention',
            field=models.BooleanField(default=False, help_text='If you set this, the check-in app will show a visible warning that tickets of this order require special attention. This will not show any details or custom message, so you need to brief your check-in staff how to handle these cases.', verbose_name='Requires special attention'),
        ),
        migrations.AlterField(
            model_name='checkinlist',
            name='include_pending',
            field=models.BooleanField(default=False, help_text='With this option, people will be able to check in even if the order have not been paid. This only works with pretixdesk 0.3.0 or newer or pretixdroid 1.9 or newer.', verbose_name='Include pending orders'),
        ),
    ]