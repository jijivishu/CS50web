# Generated by Django 4.2.2 on 2023-07-08 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pfp',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
