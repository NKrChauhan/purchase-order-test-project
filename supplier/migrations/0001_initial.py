# Generated by Django 5.0.1 on 2024-01-06 18:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256)),
                ('email', models.EmailField(max_length=256)),
            ],
            options={
                'verbose_name': 'Supplier',
                'verbose_name_plural': 'Suppliers',
                'db_table': 'suppliers',
            },
        ),
        migrations.CreateModel(
            name='LineItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=256)),
                ('quantity', models.IntegerField()),
                ('price_without_tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax_name', models.CharField(max_length=124)),
                ('tax_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('line_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_order', models.ForeignKey(help_text='Purchase Order', on_delete=django.db.models.deletion.CASCADE, to='order.purchaseorder')),
            ],
            options={
                'verbose_name': 'Line Item',
                'verbose_name_plural': 'Line Items',
                'db_table': 'line_items',
            },
        ),
    ]
