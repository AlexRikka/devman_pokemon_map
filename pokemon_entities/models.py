from django.db import models  # noqa F401
from django.utils.timezone import localtime


class Pokemon(models.Model):
    """Покемон."""

    title = models.CharField(max_length=200,
                             verbose_name='Русское название')
    title_en = models.CharField(max_length=200,
                                blank=True,
                                verbose_name='Английское название')
    title_jp = models.CharField(max_length=200,
                                blank=True,
                                verbose_name='Японское название')
    image = models.ImageField(upload_to='pokemon_images',
                              default='default.png',
                              blank=True,
                              verbose_name='Изображение')
    description = models.TextField(blank=True,
                                   verbose_name='Описание')
    previous_evolution = models.ForeignKey('self',
                                           null=True,
                                           blank=True,
                                           on_delete=models.SET_NULL,
                                           related_name='next_evolutions',
                                           verbose_name='Из кого \
                                               эволюционирует')

    def __str__(self) -> str:
        return self.title


class PokemonEntity(models.Model):
    """Единичная особь покемона на карте."""

    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                related_name='entities',
                                verbose_name='Покемон')
    lat = models.FloatField(verbose_name='Широта')
    lon = models.FloatField(verbose_name='Долгота')
    appeared_at = models.DateTimeField(default=localtime(),
                                       blank=True,
                                       verbose_name='Дата и время появления')
    disappeared_at = models.DateTimeField(default=localtime(),
                                          blank=True,
                                          verbose_name='Дата и время \
                                              исчезновения')
    level = models.IntegerField(default=0,
                                blank=True,
                                verbose_name='Уровень')
    health = models.IntegerField(default=0,
                                 blank=True,
                                 verbose_name='Здоровье')
    strength = models.IntegerField(default=0,
                                   blank=True,
                                   verbose_name='Сила')
    defence = models.IntegerField(default=0,
                                  blank=True,
                                  verbose_name='Защита')
    stamina = models.IntegerField(default=0,
                                  blank=True,
                                  verbose_name='Выносливость')
