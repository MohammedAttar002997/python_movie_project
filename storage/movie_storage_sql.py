from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///data/movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster TEXT NOT NULL
        )
    """))
    connection.commit()


def list_movies():
    """
    Retrieves all movie records from the database.

    Returns:
        dict: A nested dictionary where the key is the movie title and the value
              is a dictionary containing 'year', 'rating', and 'poster'.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating,poster FROM movies"))
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2],"poster":row[3]} for row in movies}


def add_movie(title, year, rating,poster):
    """
    Inserts a new movie record into the database.

    Args:
        title (str): The unique title of the movie.
        year (int): The release year of the movie.
        rating (float): The IMDb or user rating.
        poster (str): The URL link to the movie poster image.
    """
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating,poster) VALUES (:title, :year, :rating,:poster)"),
                               {"title": title, "year": year, "rating": rating, "poster": poster})
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """
    Removes a movie record from the database by its title.

    Args:
        title (str): The title of the movie to be deleted.
    """
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE title = :title"),
                               {"title": title})
            connection.commit()
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """
        Updates the rating of an existing movie record.

        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating value to be applied.
        """
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"),
                               {"title": title,"rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")
    pass
