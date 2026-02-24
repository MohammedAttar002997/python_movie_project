import os
import random as rnd
import requests
import statistics
from fuzzywuzzy import fuzz
from dotenv import load_dotenv
from storage import movie_storage_sql as storage
from ui.website_generator import load_html_data, serialize_movie, save_to_html

COLOR_FORMAT_MAP = {
    "user_choice_format": ['\x1b[6;30;42m', '\x1b[0m'],
    "wrong_choice_format": ['\x1b[0;30;47m', '\x1b[0m'],
}
MENU = {0: "Exit",
        1: ".List movies",
        2: ".Add movie",
        3: ".Delete movie",
        4: ".Update movie",
        5: ".Stats",
        6: ".Random movie",
        7: ".Search movie",
        8: ".Movies sorted by rating",
        9: ".Generate movie website"}

load_dotenv()

MOVIES_API_KEY = os.getenv('API_KEY')
MOVIES_URL = f"https://www.omdbapi.com/?apikey={MOVIES_API_KEY}&t="




# Getting The User Choice
def user_choice():
    """
        Displays the main menu and handles user navigation through the application.

        This function acts as the central controller, calling specific functions
        based on the integer input provided by the user.
        """

    # Get the list of movies from the database
    movies_data = storage.list_movies()



    # Checking user choice
    try:
        while True:
            # Looping over the menu to show it for the user
            for num, value in MENU.items():
                print(
                    COLOR_FORMAT_MAP["user_choice_format"][0] + str(num) + str(value) +
                    COLOR_FORMAT_MAP["user_choice_format"][
                        1])
            print()
            choice = int(input("\nEnter choice (0 - 9): ").strip())
            if choice not in range(10) or choice == "":
                print(COLOR_FORMAT_MAP["wrong_choice_format"][0] + "Invalid choice. Please enter a valid choice." +
                      COLOR_FORMAT_MAP["wrong_choice_format"][1])
                choice = int(input("Enter choice (1-9): ").strip())
            match choice:
                case 0:
                    quit("Exiting the program. Goodbye!")
                case 1:
                    movies_data = storage.list_movies()
                    print()
                    movies_list(movies_data)
                case 2:
                    add_movie(movies_data)
                case 3:
                    del_movie(movies_data)
                case 4:
                    update_movie(movies_data)
                case 5:
                    movies_stats(movies_data)
                case 6:
                    random_movie(movies_data)
                case 7:
                    search_movie(movies_data)
                case 8:
                    sorted_by_rating(movies_data)
                case 9:
                    movies_data = storage.list_movies()
                    generate_movie(movies_data)
    except requests.exceptions.Timeout:
        print("\nError: The request timed out. Please check your internet connection.")
    except requests.exceptions.RequestException as e:
        print(f"\nError: A network error occurred: {e}")
    except Exception as exception:
        print(f"\nAn unexpected error occurred: {exception}")

# Showing movies list
def movies_list(movies):
    """
        Prints a formatted list of all movies currently in the database.

        Args:
            movies (dict): A dictionary where keys are movie titles and values
                           are dictionaries containing 'year' and 'rating'.
        """
    print(f"{len(movies)} movies in total")
    for movie,data in movies.items():
        print(f"{movie} ({data["year"]}): {data["rating"]}")
    print()


# Add movie
def add_movie(movies):
    """
        Prompts the user for a movie title, fetches its details from the OMDb API,
        and saves it to the database.

        Args:
            movies (dict): The current movie dataset used to check for duplicates.
        """
    try:
        movie_name = input("Enter movie name: ")

        final_url = MOVIES_URL+movie_name
        response = requests.get(final_url)
        res = response.json()
        while res.get("Response") == "False":
            print(res["Error"]+"\n")
            movie_name = input("Enter movie name or press q to go back to the main menu: ")
            if movie_name == "q":
                print("\nReturning to main menu...\n")
                return
            final_url = MOVIES_URL + movie_name
            response = requests.get(final_url)
            res = response.json()
        if res["Title"] in movies:
            storage.list_movies()
            print("Movie already exists please use the (List movies command to see the available movies)")
        else:
            storage.add_movie(res["Title"],res["Year"], res["imdbRating"],res["Poster"])
        print(f"\nMovie {res["Title"]} has been added")
    except requests.exceptions.Timeout:
        print("\nError: The request timed out. Please check your internet connection.")
    except requests.exceptions.RequestException as e:
        print(f"\nError: A network error occurred: {e}")
    except Exception as exception:
        print(f"\nAn unexpected error occurred: {exception}")


# Update movie rating
def update_movie(movies):
    """
        Updates the rating of an existing movie in the database.

        Args:
            movies (dict): The current movie dataset to verify movie existence.
        """
    movie_name = input("Enter movie name: ")
    while movie_name not in movies:
        movie_name = input(
            f"Movie name {movie_name} does not exist please enter a valid movie name or press q to exit: ")
        if movie_name == "q":
            print("\nReturning to main menu...\n")
            return
    movie_rating = float(input("Enter new movie rating (0-10): "))
    while 0.0 > movie_rating or movie_rating > 10.0:
        movie_rating = float(input(f"Rating {movie_rating} is invalid please enter another rating: "))
    movies[movie_name]["movie_rating"] = movie_rating
    # ms.update_movie(movie_name, movie_rating)
    print(f"Movie {movie_name} has been updated")


# Delete a movie
def del_movie(movies):
    """
        Removes a movie from the database based on the user's input.

        Args:
            movies (dict): The current movie dataset to verify movie existence.
        """
    movie_name = input("Enter movie name: ")
    while movie_name not in movies:
        movie_name = input(f"Movie {movie_name} does not exist please enter a valid movie name or press q to exit:")
        if movie_name == "q":
            print("\nReturning to main menu...\n")
            return
    storage.delete_movie(movie_name)
    print(f"Movie {movie_name} has been deleted")


# Showing movie stats
def movies_stats(movies):
    """
        Calculates and prints statistics about the movie collection, including
        average rating, median rating, and the best/worst performing movies.

        Args:
            movies (dict): The movie dataset used for statistical calculations.
        """
    max_key = ""
    max_value = 0.0
    min_key = ""
    min_value = 0.0
    rating_sum = 0.0
    median_rating = []
    for movie, value in movies.items():
        if min_value == 0:
            min_value = value["rating"]
        if value["rating"] > max_value:
            max_key = movie
            max_value = value["rating"]
        if value["rating"] < min_value:
            min_value = value["rating"]
            min_key = movie
        rating_sum += value["rating"]
        median_rating.append(value["rating"])
    print(f"Average rating: {round(rating_sum / len(movies),2)}")
    print(f"Median rating: {statistics.median(median_rating)}")
    print(f"Best movie: {max_key}, {max_value}")
    print(f"Worst movie: {min_key}, {min_value}")
    # print(f"best movie is {max(movies, key=movies.get)},")
    # print(f"worst movie is {min(movies, key=movies.get)}")


# Suggesting a random movie for the user
def random_movie(movies):
    """
        Selects and displays a single random movie from the collection.

        Args:
            movies (dict): The movie dataset to pick from.
        """
    rand_value = rnd.sample(list(movies.items()), 1)
    print(
        f"Your movie for tonight: {rand_value[0][0]} ({rand_value[0][1]["year"]}), it's rated {rand_value[0][1]["rating"]}")


# Search a movie
def search_movie(movies):
    """
        Searches the collection for movies matching a user's query using fuzzy string matching.

        Args:
            movies (dict): The movie dataset to search within.
        """
    query = input("Enter part of movie name: ")
    for movie, value in movies.items():
        # if query in movie:
        if fuzz.partial_ratio(query.lower(), movie.lower()) > 60:
            print(movie, value["rating"])


# Sort movies in descending order by rating
def sorted_by_rating(movies):
    """
        Displays the entire movie collection sorted in descending order by rating.

        Args:
            movies (dict): The movie dataset to be sorted.
        """
    value = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    print("\n\n")
    for movie, rating in value:
        print(movie, rating["rating"])


def generate_movie(movies):
    """
        Generates a static HTML website (movies.html) representing the movie collection.

        This function reads an HTML template, injects serialized movie data into the
        grid, and saves the final file to the filesystem.

        Args:
            movies (dict): The movie dataset used to populate the website.
        """
    movie_html_data = load_html_data('_static/index_template.html')
    output = ''  # define an empty string
    for movie,value in movies.items():
        output += serialize_movie(movie,value)

    new_html_data = movie_html_data.replace('__TEMPLATE_MOVIE_GRID__', output)
    save_to_html(new_html_data, '_static/movies.html')
    print("Website was generated successfully.\n")


# Our main function where our movies app first launch
def main():
    """
        The main entry point of the application.
        Initializes the program and launches the user interface.
        """
    title = "*" * 7 + " Welcome to my movies app " + "*" * 7
    print(title, end="\n\n")
    # Your code here
    user_choice()


if __name__ == "__main__":
    main()
