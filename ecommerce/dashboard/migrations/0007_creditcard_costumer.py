# Generated by Django 3.2.4 on 2021-07-03 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_costumer_photo'),
        ('dashboard', '0006_remove_creditcard_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='costumer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shop.costumer'),
            preserve_default=False,
        ),
    ]
