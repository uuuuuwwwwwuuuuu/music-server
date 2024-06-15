from rest_framework import generics
from rest_framework.decorators import api_view

from .models import Track
from User.models import User
from .serializers import TrackSerializer
from rest_framework.response import Response

from random import choice



class TrackApiViewAll(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class TrackApiViewGetFiltered(generics.ListAPIView):
    serializer_class = TrackSerializer

    def post(self, request):
        title = request.data.get('title')
        artists = request.data.get('artists')
        if title or artists:
            lst = Track.objects.all()
            track_list = list(lst)

            if title and artists:
                queryset = filter(lambda track: str(title).lower() in track.title.lower() and str(artists.lower()) in track.artists.lower(), track_list)
            else:
                queryset = filter(lambda track: str(title).lower() in track.title.lower() or str(artists).lower() in track.artists.lower(), track_list)

            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"data": "Треки не найдены"})

@api_view(['GET'])
def TrackApiViewGetLiked(request):
    token = request.headers.get('Token')
    user = User.objects.filter(self_token=token).first()

    if not user:
        return Response({"error": "Пользователь не идентифицирован"})

    serializer = TrackSerializer(user.liked_track_list.all(), many=True)

    return Response({"data": serializer.data})

@api_view(['POST'])
def TrackApiViewAddAudition(request):
    trackId = request.data.get('trackId')

    try:
        track = Track.objects.filter(id=trackId).first()
    except:
        return Response({'error': 'Не удалось зафиксировать прослушивание'})
    track.auditions += 1
    track.save()

    return Response({'data': 'Прослушивание засчитано'})

@api_view(['POST'])
def GetArtistTracks(request):
    tracksId = request.data.get('tracks')

    try:
        trackList = []
        for track in tracksId:
            trackItem = Track.objects.filter(id=track).first()
            trackList.append(trackItem)
    except:
        return Response({'error': 'Произошла ошибка'})

    serializer = TrackSerializer(trackList, many=True)
    return Response({'data': serializer.data})
