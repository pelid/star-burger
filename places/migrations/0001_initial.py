# Generated by Django 3.0.7 on 2021-04-26 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=150, verbose_name='адрес')),
                ('lat', models.FloatField(verbose_name='широта')),
                ('lon', models.FloatField(verbose_name='долгота')),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='дата обновления')),
            ],
        ),
    ]