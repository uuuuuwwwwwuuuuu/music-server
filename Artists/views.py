from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Artists.models import Artist
from Artists.serializers import ArtistsSerializer

class GetArtists(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistsSerializer

