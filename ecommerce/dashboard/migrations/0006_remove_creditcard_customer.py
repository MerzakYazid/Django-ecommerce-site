# Generated by Django 3.2.4 on 2021-07-03 17:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_creditcard_cvv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditcard',
            name='customer',
        ),
    ]
