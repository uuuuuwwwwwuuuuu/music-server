from django.urls import path
from Artists.views import *

urlpatterns = [
    path('artists/', GetArtists.as_view()),
]