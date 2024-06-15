from django.db import models

from usefull_functions import generate_id


class Track(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=155, verbose_name='Название')
    artists = models.CharField(max_length=200, verbose_name='Артисты')
    id = models.CharField(max_length=40, primary_key=True, editable=False, unique=True, blank=True)
    albumImg = models.ImageField(upload_to='albumsImg/')
    music = models.FileField(upload_to='music/')
    auditions = models.BigIntegerField(blank=True, default=0)

    def __str__(self):
        return f'{self.title} | {self.artists}'

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = generate_id(40)

        super().save(*args, **kwargs)
