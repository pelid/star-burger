# Generated by Django 3.0.7 on 2021-03-26 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0043_auto_20210326_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Наличные'), ('card', 'Банковская карта')], default='', max_length=15, verbose_name='Способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('no', 'Не обработан'), ('yes', 'Обработан')], default='no', max_length=15, verbose_name='Статус'),
        ),
    ]
