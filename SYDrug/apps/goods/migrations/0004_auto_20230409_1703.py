# Generated by Django 3.1 on 2023-04-09 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20230409_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsimage',
            name='sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.goodssku', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='indexgoodsbanner',
            name='sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.goodssku', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='indextypegoodsbanner',
            name='sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.goodssku', verbose_name='商品SKU'),
        ),
        migrations.AlterField(
            model_name='indextypegoodsbanner',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='goods.goodstype', verbose_name='商品类型'),
        ),
    ]
