# Generated by Django 4.2.2 on 2023-07-10 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_rename_likes_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(null=True, upload_to='posts/'),
        ),
    ]
