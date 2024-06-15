from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from Track.models import Track
from .serializers import *
from .models import User
from Artists.serializers import *

from usefull_functions import encrypt_string
from Track.serializers import TrackSerializer


class UserApiViewAll(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserApiViewCreate(generics.CreateAPIView):
    serializer_class = UserSerializerCreate

    def post(self, request, *args, **kwargs):
        same_user = User.objects.filter(username=request.data['username'])
        if same_user:
            return Response({'error': 'Такой пользователь уже существует'})

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'data': 'Пользователь зарегистрирован'})


class UserApiViewAuth(generics.RetrieveUpdateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            hashed_password = encrypt_string(request.data['password'])
        except:
            return Response({'error': 'Вы не ввели пароль'})
        user = User.objects.filter(username=request.data['username'], password=hashed_password).first()

        if not user:
            return Response({'error': 'Не правильный логин или пароль'})

        if not user.self_token:
            user.self_token = generate_token(user.username, user.password)
            user.save()
        return Response({'token': user.self_token})


class UserApiViewLogout(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        token = request.headers.get('Token')

        if not token:
            return Response({"error": 'Доступ не предоставлен'})

        user = User.objects.filter(self_token=token).first()

        if not user:
            return Response({'error': 'Недествительный токен, обратитесь в тех поддержку'})

        user.self_token = ''
        user.save()
        return Response({"data": "Вы успешно вышли из системы"})


class UserApiViewDestroy(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        token = request.headers.get("Token")

        if not token:
            return Response({"error": 'Доступ не предоставлен'})

        user = User.objects.filter(self_token=token).first()

        if not user:
            return Response({'error': 'Недествительный токен, обратитесь в тех поддержку'})

        user.delete()
        return Response({"data": "Аккаунт успешно удалён"})


class UserApiViewGetOne(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'self_token'


@api_view(['PUT'])
def userApiViewToggleLiked(request):
    token = request.headers.get('Token')
    data = request.data
    user = User.objects.filter(self_token=token).first()
    if not user:
        return Response({"error": "Пользователь не идентифицирован"})

    serializer = UserSerializerToggle(data=data, instance=user)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    trackList = []
    for trackId in serializer.data['liked_track_list']:
        track = Track.objects.filter(id=trackId).first()
        trackList.append(track)

    track_serializer = TrackSerializer(data=trackList, many=True)
    track_serializer.is_valid()

    return Response({'data': track_serializer.data})


@api_view(['PUT'])
def userApiViewToggleArtist(request):
    token = request.headers.get('Token')
    artistId = request.data
    user = User.objects.filter(self_token=token).first()

    if not user:
        return Response({"error": "Пользователь не идентифицирован"})

    serializer = UserSerializerToggleArtists(data=artistId, instance=user)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    artist_list = []
    for artist_id in serializer.data['liked_artists']:
        artist = Artist.objects.filter(id=artist_id).first()
        artist_list.append(artist)

    artist_serializer = ArtistsSerializer(data=artist_list, many=True)
    artist_serializer.is_valid()

    return Response(artist_serializer.data)


@api_view(['GET'])
def getLikedArtists(request):
    token = request.headers.get('Token')
    user = User.objects.filter(self_token=token).first()

    if not user:
        return Response({"error": "Пользователь не идентифицирован"})

    serializer = ArtistsSerializer(user.liked_artists.all(), many=True)

    return Response(serializer.data)


@api_view(['PUT'])
def setUserImg(request):
    token = request.headers.get('Token')
    data = request.data
    user = User.objects.filter(self_token=token).first()

    if not user:
        return Response({'error': 'Пользователь не идентифицирован'})

    serializer = UserSerializerPhoto(data=data, instance=user)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response(serializer.data)
