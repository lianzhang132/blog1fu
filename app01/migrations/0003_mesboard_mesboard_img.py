# Generated by Django 2.1.5 on 2019-06-29 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_mesboard'),
    ]

    operations = [
        migrations.AddField(
            model_name='mesboard',
            name='mesboard_img',
            field=models.CharField(default='null', max_length=999),
        ),
    ]