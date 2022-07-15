# Generated by Django 4.0.5 on 2022-07-08 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_profiles_about_profiles_friends'),
    ]

    operations = [
        migrations.CreateModel(
            name='friends',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='base.profiles')),
            ],
        ),
        migrations.DeleteModel(
            name='myfriends',
        ),
        migrations.AlterField(
            model_name='profiles',
            name='friends',
            field=models.ManyToManyField(blank=True, to='base.friends'),
        ),
    ]
