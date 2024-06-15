from rest_framework.urls import path
from .views import *

urlpatterns = [
    path('users/', UserApiViewAll.as_view()),
    path('users/register/', UserApiViewCreate.as_view()),
    path('users/auth/', UserApiViewAuth.as_view()),
    path('users/logout/', UserApiViewLogout.as_view()),
    path('users/destroy/', UserApiViewDestroy.as_view()),
    path('users/getdata/<str:self_token>/', UserApiViewGetOne.as_view()),
    path('users/toggleliked/', userApiViewToggleLiked),
    path('users/toggleartists/', userApiViewToggleArtist),
    path('users/getlikedartists/', getLikedArtists),
    path('users/setuserphoto/', setUserImg)
]