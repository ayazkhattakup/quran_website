# Generated by Django 5.0.6 on 2024-05-22 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src_app', '0005_alter_order_ordered_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivered_on',
            field=models.DateField(null=True, verbose_name='Delivered On'),
        ),
    ]
