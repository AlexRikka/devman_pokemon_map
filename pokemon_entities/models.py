from django.db import models  # noqa F401


class Pokemon(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True,
                              upload_to='pokemon_images')

    def __str__(self) -> str:
        return f'{self.title}'
