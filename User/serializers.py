from rest_framework import serializers
from .models import User
from rest_framework.exceptions import ValidationError
from usefull_functions import encrypt_string, generate_token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'reg_date', 'user_img']


class UserSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'user_img']

    def create(self, validated_data):
        data = validated_data
        data['password'] = encrypt_string(data['password'])
        return User.objects.create(**data)


class UserSerializerToggle(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['liked_track_list']

    def update(self, instance, validated_data):
        if validated_data['liked_track_list'][0] not in instance.liked_track_list.all():
            instance.liked_track_list.add(*validated_data['liked_track_list'])
            instance.save()
        else:
            instance.liked_track_list.remove(*validated_data['liked_track_list'])
            instance.save()

        return instance


class UserSerializerToggleArtists(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['liked_artists']

    def update(self, instance, validated_data):
        if validated_data['liked_artists'][0] not in instance.liked_artists.all():
            instance.liked_artists.add(*validated_data['liked_artists'])
            instance.save()
        else:
            instance.liked_artists.remove(*validated_data['liked_artists'])
            instance.save()

        return instance


class UserSerializerPhoto(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_img']

    def update(self, instance, validated_data):
        instance.user_img = validated_data['user_img']
        instance.save()
        return instance
