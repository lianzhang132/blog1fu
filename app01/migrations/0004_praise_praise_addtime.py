# Generated by Django 2.1.5 on 2019-07-01 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_mesboard_mesboard_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='praise',
            name='praise_addtime',
            field=models.DateField(default=None),
        ),
    ]
