# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('ip_address', models.GenericIPAddressField(null=True, blank=True)),
                ('user_agent', models.CharField(null=True, max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('client_date', models.DateTimeField(null=True, blank=True)),
                ('server_date', models.DateTimeField(auto_now_add=True)),
                ('path', models.CharField(max_length=255)),
                ('referer', models.TextField(null=True, blank=True)),
                ('action', models.CharField(default='view', max_length=255)),
                ('data', models.TextField(null=True, blank=True)),
            ],
            options={
                'ordering': ['-server_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('client_key', models.CharField(null=True, max_length=255, blank=True)),
                ('server_key', models.CharField(null=True, max_length=255, blank=True)),
                ('client', models.ForeignKey(to='owl.Client')),
                ('user', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('user', 'client_key', 'server_key')]),
        ),
        migrations.AddField(
            model_name='event',
            name='session',
            field=models.ForeignKey(null=True, to='owl.Session', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='client',
            unique_together=set([('ip_address', 'user_agent')]),
        ),
    ]
