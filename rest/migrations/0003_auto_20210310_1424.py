# Generated by Django 3.1.7 on 2021-03-10 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0002_courierworkinghour_orderdeliveryhour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courier',
            name='working_hours',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_hours',
        ),
    ]