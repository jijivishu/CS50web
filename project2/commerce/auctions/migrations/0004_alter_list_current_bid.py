# Generated by Django 4.2.2 on 2023-06-11 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_list_category_alter_list_current_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='current_bid',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
