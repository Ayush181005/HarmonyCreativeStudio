# Generated by Django 3.2 on 2021-08-15 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_alter_portfolio_img1'),
    ]

    operations = [
        migrations.CreateModel(
            name='broadcasted_message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg', models.TextField()),
            ],
        ),
    ]
