# Generated by Django 4.0.5 on 2022-07-08 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_alter_myfriends_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profiles',
            name='friends',
        ),
    ]
