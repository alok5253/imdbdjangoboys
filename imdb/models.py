from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

#Create your models here.
class Genre(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)
        db_table = 'genre_table'

class Movie(models.Model):
    owner = models.ForeignKey('auth.User', related_name='movies')
    popularity99 = models.DecimalField(decimal_places=1, max_digits=3, validators=[MinValueValidator(0.0),MaxValueValidator(100.0)])
    director = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    imdb_score = models.DecimalField(decimal_places=1, max_digits=2, validators=[MinValueValidator(0.0),MaxValueValidator(10.0)])
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        db_table = 'movie_table'