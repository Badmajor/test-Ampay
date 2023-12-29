# Generated by Django 4.2.8 on 2023-12-29 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_discount_tax_order_discount_order_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='currency',
            field=models.CharField(choices=[('usd', 'usd'), ('eur', 'eur')], default='usd', max_length=3),
        ),
    ]