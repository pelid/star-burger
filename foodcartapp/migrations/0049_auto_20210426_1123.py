# Generated by Django 3.0.7 on 2021-04-26 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_auto_20210426_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('cash', 'Наличные'), ('card', 'Банковская карта')], max_length=15, verbose_name='Способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='foodcartapp.Restaurant', verbose_name='Ресторан'),
        ),
    ]
