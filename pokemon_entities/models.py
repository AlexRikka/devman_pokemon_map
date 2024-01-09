from django.db import models  # noqa F401
from django.utils.timezone import now


class Pokemon(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True,
                              upload_to='pokemon_images')

    def __str__(self) -> str:
        return f'{self.title}'


class PokemonEntity(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(default=now)
    disappeared_at = models.DateTimeField(default=now)
