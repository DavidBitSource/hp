# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 19:05
from __future__ import unicode_literals

import antispam.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlockedEmail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('address', models.EmailField(max_length=254, unique=True)),
                ('expires', models.DateTimeField(default=antispam.models._default_email_expires)),
            ],
            options={
                'abstract': False,
            },
            bases=(antispam.models.BlockedMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BlockedIpAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('address', models.GenericIPAddressField(unique=True)),
                ('expires', models.DateTimeField(default=antispam.models._default_ipaddress_expires)),
            ],
            options={
                'abstract': False,
            },
            bases=(antispam.models.BlockedMixin, models.Model),
        ),
    ]