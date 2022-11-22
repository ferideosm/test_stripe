# Generated by Django 4.1.3 on 2022-11-18 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_discount_order_tax_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.discount'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='tax',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.tax'),
        ),
    ]