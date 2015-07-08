# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owl', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('client', 'user', 'client_key', 'server_key')]),
        ),
    ]
