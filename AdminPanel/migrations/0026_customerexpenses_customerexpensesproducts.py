# Generated by Django 4.2 on 2023-06-05 10:22

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AdminPanel', '0025_alter_supplierexpenses_expensetype'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerExpenses',
            fields=[
                ('billNo', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('expenseType', models.CharField(max_length=100)),
                ('billDate', models.DateField(default=datetime.date.today)),
                ('customerName', models.CharField(max_length=100)),
                ('customerPhone', models.CharField(max_length=12)),
                ('customerGst', models.CharField(max_length=50)),
                ('paymentType', models.CharField(max_length=10)),
                ('total', models.FloatField()),
                ('gst', models.FloatField(default=0)),
                ('grossTotal', models.FloatField(default=0)),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Customer Expenses',
            },
        ),
        migrations.CreateModel(
            name='CustomerExpensesProducts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('product', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('unit', models.CharField(max_length=50)),
                ('pricePerUnit', models.IntegerField()),
                ('amount', models.IntegerField()),
                ('billNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminPanel.customerexpenses')),
            ],
            options={
                'verbose_name_plural': 'Customer Expenses Products',
            },
        ),
    ]