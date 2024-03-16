# Generated by Django 4.2 on 2023-05-24 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPanel', '0015_alter_productmodel_quantity_sold'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productmodel',
            old_name='productprice',
            new_name='purchaseprice',
        ),
        migrations.AddField(
            model_name='productmodel',
            name='sellprice',
            field=models.IntegerField(default=0, null=True),
        ),
    ]