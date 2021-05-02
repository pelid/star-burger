from django.db import models


class Place(models.Model):
    address = models.CharField('адрес', max_length=150, unique=True)
    lat = models.FloatField('широта')
    lon = models.FloatField('долгота')
    update_date = models.DateTimeField('дата обновления', auto_now=True, db_index=True)
