from rest_framework import serializers
from imdb.models import Movie, Genre


# Defining Serializers here.
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('title',)


class MovieSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='title'
     )

    class Meta:
        model = Movie
        fields = ('owner','popularity99','director','genre','imdb_score','name')


class MovieDetailsSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='title'
     )

    class Meta:
        model = Movie
        fields = ('popularity99','director','genre','imdb_score','name')
