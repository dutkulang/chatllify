# Generated by Django 4.0.5 on 2022-07-18 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_personalmessages_options_remove_profiles_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='profile_pics',
            field=models.ImageField(default='image.jpg', upload_to='profile_images'),
        ),
    ]
