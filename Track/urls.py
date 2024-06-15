from django.urls import path

from Track.views import *

urlpatterns = [
    path('tracks/', TrackApiViewAll.as_view()),
    path('tracks/filter/', TrackApiViewGetFiltered.as_view()),
    path('tracks/getliked/', TrackApiViewGetLiked),
    path('tracks/addaudition/', TrackApiViewAddAudition),
    path('tracks/getartisttracks/', GetArtistTracks)
]