# Generated by Django 4.1.2 on 2022-11-30 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrumboard', '0004_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='from_user',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='message',
            name='to_user',
            field=models.IntegerField(default=None),
        ),
    ]
