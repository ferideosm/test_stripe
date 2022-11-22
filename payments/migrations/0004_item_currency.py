# Generated by Django 4.1.3 on 2022-11-18 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_alter_orderitem_discount_alter_orderitem_tax'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='currency',
            field=models.CharField(blank=True, choices=[('EUR', 'Eur'), ('USD', 'Usd')], default='USD', max_length=5),
        ),
    ]