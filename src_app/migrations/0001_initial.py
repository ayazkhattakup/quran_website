# Generated by Django 5.0.6 on 2024-05-20 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Book Title')),
                ('img', models.ImageField(default='', upload_to='Books', verbose_name='Book Image')),
                ('price', models.PositiveIntegerField(verbose_name='Price')),
                ('available', models.BooleanField(default=True, verbose_name='Book Available?')),
            ],
        ),
        migrations.CreateModel(
            name='Reciter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3000, verbose_name="Reciter's Name")),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=1000, verbose_name='Gender')),
                ('country', models.CharField(max_length=1000, verbose_name="Reciter's Country of Residence")),
                ('img', models.ImageField(blank=True, default='', upload_to='reciters', verbose_name="Reciter's Picture")),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False, verbose_name='Order Status(Completionn)')),
                ('ordered_on', models.DateField(auto_now_add=True, verbose_name='Ordered On')),
                ('delivered_on', models.DateField(verbose_name='Delivered On')),
                ('total_price', models.PositiveIntegerField(default='Total Price')),
                ('address', models.TextField(default='', verbose_name='Delivery Address')),
                ('contact', models.CharField(max_length=1000, verbose_name='Contact Number')),
                ('payment_method', models.CharField(choices=[('Paypal', 'Paypal'), ('Stripe', 'Stripe'), ('Cash on delivery', 'Cash on delivery')], max_length=1000, verbose_name='Payment Method')),
                ('payment_done', models.BooleanField(default=False, verbose_name='Payment Complete')),
                ('books', models.ManyToManyField(to='src_app.book', verbose_name='Ordered Books')),
            ],
        ),
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100000, verbose_name='Title')),
                ('audio_file', models.FileField(default='', upload_to='Tilawahs', verbose_name='Audio File')),
                ('kind', models.CharField(choices=[('few_verses', 'few_verses'), ('surah', 'surah')], max_length=1000, null=True)),
                ('reciter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src_app.reciter', verbose_name='Reciter')),
            ],
        ),
    ]
