# Generated by Django 3.1 on 2023-04-09 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20230409_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsimage',
            name='sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodssku', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='goodssku',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goods', verbose_name='商品SPU'),
        ),
        migrations.AlterField(
            model_name='goodssku',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodstype', verbose_name='商品种类'),
        ),
        migrations.AlterField(
            model_name='indexgoodsbanner',
            name='sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodssku', verbose_name='商品'),
        ),
        migrations.AlterField(
            model_name='indextypegoodsbanner',
            name='sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodssku', verbose_name='商品SKU'),
        ),
        migrations.AlterField(
            model_name='indextypegoodsbanner',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodstype', verbose_name='商品类型'),
        ),
    ]
