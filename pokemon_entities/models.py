from django.db import models  # noqa F401
from django.utils.timezone import localtime


class Pokemon(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, default='', blank=True)
    title_jp = models.CharField(max_length=200, default='', blank=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to='pokemon_images')
    description = models.TextField(default='', blank=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f'{self.title}'


class PokemonEntity(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(default=localtime())
    disappeared_at = models.DateTimeField(default=localtime())
    level = models.IntegerField(default=0)
    health = models.IntegerField(default=0)
    strength = models.IntegerField(default=0)
    defence = models.IntegerField(default=0)
    stamina = models.IntegerField(default=0)
