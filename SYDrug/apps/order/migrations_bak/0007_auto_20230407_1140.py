# Generated by Django 3.1 on 2023-04-07 03:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20230407_1128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.orderinfo', verbose_name='订单'),
        ),
    ]