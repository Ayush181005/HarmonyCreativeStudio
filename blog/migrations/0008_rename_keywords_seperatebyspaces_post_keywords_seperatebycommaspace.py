# Generated by Django 3.2 on 2021-07-06 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20210630_1957'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='keywords_seperateBySpaces',
            new_name='keywords_seperateByCommaSpace',
        ),
    ]
