from django.db import models

from Artists.models import Artist
from Track.models import Track


class User(models.Model):
    username = models.CharField(max_length=155)
    password = models.TextField()
    email = models.CharField(max_length=255)
    liked_track_list = models.ManyToManyField(Track)
    self_token = models.CharField(max_length=40, blank=True)
    reg_date = models.DateTimeField(auto_now_add=True)
    liked_artists = models.ManyToManyField(Artist)
    user_img = models.ImageField(upload_to='userImg/', blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.username
