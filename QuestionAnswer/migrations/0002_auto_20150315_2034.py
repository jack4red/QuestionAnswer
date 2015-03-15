# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('QuestionAnswer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 15, 15, 4, 29, 659551, tzinfo=utc), verbose_name=b'date posted'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 15, 15, 4, 37, 261125, tzinfo=utc), verbose_name=b'date posted'),
            preserve_default=False,
        ),
    ]
