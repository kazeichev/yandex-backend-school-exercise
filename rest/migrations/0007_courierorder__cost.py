# Generated by Django 3.1.7 on 2021-03-23 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0006_auto_20210322_0706'),
    ]

    operations = [
        migrations.AddField(
            model_name='courierorder',
            name='_cost',
            field=models.IntegerField(db_column='cost', default=None),
        ),
    ]
