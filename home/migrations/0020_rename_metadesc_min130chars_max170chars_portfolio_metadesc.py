# Generated by Django 3.2 on 2021-07-21 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_rename_photo_644x641px_teammember_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='portfolio',
            old_name='metaDesc_min130Chars_max170Chars',
            new_name='metaDesc',
        ),
    ]
