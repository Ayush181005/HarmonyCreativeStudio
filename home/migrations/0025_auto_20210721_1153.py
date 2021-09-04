# Generated by Django 3.2 on 2021-07-21 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_alter_teammember_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='photo_height',
            field=models.IntegerField(default=641),
        ),
        migrations.AddField(
            model_name='teammember',
            name='photo_width',
            field=models.IntegerField(default=644),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='photo',
            field=models.ImageField(height_field='photo_height', help_text='644x641px', upload_to='home/our_team', width_field='photo_width'),
        ),
    ]
