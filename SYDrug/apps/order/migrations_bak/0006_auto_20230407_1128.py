# Generated by Django 3.1 on 2023-04-07 03:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20230407_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='order',
            field=models.ForeignKey(db_constraint='df_order_goods_order_id_fk_df_order_info_order_id', on_delete=django.db.models.deletion.CASCADE, to='order.orderinfo', verbose_name='订单'),
        ),
        migrations.AlterField(
            model_name='orderinfo',
            name='order_id',
            field=models.CharField(max_length=128, primary_key=True, serialize=False, verbose_name='订单id'),
        ),
    ]