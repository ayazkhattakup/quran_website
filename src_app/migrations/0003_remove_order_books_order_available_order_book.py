# Generated by Django 5.0.6 on 2024-05-20 19:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src_app', '0002_book_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='books',
        ),
        migrations.AddField(
            model_name='order',
            name='available',
            field=models.BooleanField(default=True, null=True, verbose_name='Product Available?'),
        ),
        migrations.AddField(
            model_name='order',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='src_app.book', verbose_name='Ordered Books'),
        ),
    ]
