from django.db import models

from Track.models import Track


class Artist (models.Model):
    name = models.CharField(max_length=255)
    artistImg = models.ImageField(upload_to='artistsImg/')
    likes = models.BigIntegerField(blank=True, default=0)
    tracks = models.ManyToManyField(Track)
    big_img = models.ImageField(upload_to='artistsBigImg/', null=True)

    objects = models.Manager()

    def __str__(self):
        return self.name


