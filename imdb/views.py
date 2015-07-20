from rest_framework import status
from rest_framework.response import Response
from imdb.models import Movie, Genre
from imdb.serializers import MovieSerializer, MovieDetailsSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from imdb.permissions import IsOwnerOrReadOnly


class MovieList(APIView):
    """
    Get List of Movies, POST a new Movie
    """
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    #Retrieve all the Movies in JSON Format
    def get(self, request, format=None):
         articles = Movie.objects.all()
         serializer = MovieDetailsSerializer(articles, many=True)
         return Response(serializer.data)

    parser_classes = (JSONParser,)

    #Create a new Movie by input as JSON Format
    def post(self, request, format=None):

        data = request.data
        count=0

        for gnr in data["genre"]:
            count = count + 1
            Genre.objects.get_or_create(title=gnr)

        if count == 0:
           return Response({"Movie Genres NOT present in the Json ***"}, status=status.HTTP_404_NOT_FOUND)

        try:
            movie_name = data["name"]
            director_name = data["director"]
            Movie.objects.get(name=movie_name, director=director_name)
            return Response({"[Movie,Director]: ["+movie_name+","+director_name+"] is Already present in the DB ***"}, status=status.HTTP_302_FOUND)
        except Movie.DoesNotExist:
            serializer = MovieSerializer(data=data)
            if serializer.is_valid():
                serializer.save(owner=self.request.user)
                return Response(serializer.initial_data, status=status.HTTP_201_CREATED)
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


class MovieFilterList(generics.ListAPIView):
    serializer_class = MovieDetailsSerializer

    def get_queryset(self):
        queryset = Movie.objects.all()

        name = self.request.query_params.get('name', None)
        rating = self.request.query_params.get('rating', None)
        director = self.request.query_params.get('director', None)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        if rating is not None:
            queryset = queryset.filter(imdb_score=rating)
        if director is not None:
            queryset = queryset.filter(director__icontains=director)
        return queryset


class MovieDetail(APIView):
    """
    Get, Udpate, and Delete a Movie Details
    """
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


    def get(self, request, pk, format=None):
        try:
            movie = Movie.objects.get(pk=pk)
            serializer = MovieDetailsSerializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({"Movie key: "+pk+" NOT present in the DB ***"}, status=status.HTTP_404_NOT_FOUND)


    def put(self, request, pk, format=None):
        try:
            movie = Movie.objects.get(pk=pk)
            data = request.data
            count=0

            for gnr in data["genre"]:
                count = count + 1
                Genre.objects.get_or_create(title=gnr)

            if count == 0:
               return Response({"Movie Genres NOT present in the Json ***"}, status=status.HTTP_404_NOT_FOUND)

            serializer = MovieSerializer(movie, data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.initial_data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Movie.DoesNotExist:
            return Response({"Movie key: "+pk+" NOT present in the DB ***"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, pk, format=None):
        try:
            movie = Movie.objects.get(pk=pk)
            movie.delete()
            return Response({"Movie key: "+pk+" is DELETED from the DB ***"}, status=status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response({"Movie key: "+pk+" NOT present in the DB ***"}, status=status.HTTP_404_NOT_FOUND)

