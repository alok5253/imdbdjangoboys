Created a RESTful API for movies(something similar to IMDB). For this I use:
1. MySql to store data,
2. Django for api.

There need to be 2 levels of access:
admin = who can add, remove or edit movies.
users = who can just view the movies.

1. Admin on login can entered data into the database in valid json format as given:

{
    "99popularity": 83.0,
    "director": "Victor Fleming",
    "genre": [
      "Adventure",
      " Family",
      " Fantasy",
      " Musical"
    ],
    "imdb_score": 8.3,
    "name": "The Wizard of Oz"
}

2. He/She can Get, Delete and Update a specific movie details into the database in valid json format as given:

{
    "99popularity": 76.0,
    "director": "Victor Fleming Jr.",
    "genre": [
      "Adventure",
      " Family",
      " Genre2",
      " Musical",
	  "Genre1"
    ],
    "imdb_score": 7.6,
    "name": "The Wizard of Oz 2"
}

3. Users can only view the list of movies or a specific movie details.





