import os
import random as rnd
import statistics
import requests
from fuzzywuzzy import fuzz
from storage import movie_storage_sql as storage
from dotenv import load_dotenv

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

    # Get the list of movies from the database

    movies_data = storage.list_movies()


    # Looping over the menu to show it for the user
    for num, value in MENU.items():
        print(
            COLOR_FORMAT_MAP["user_choice_format"][0] + str(num) + str(value) + COLOR_FORMAT_MAP["user_choice_format"][
                1])
    print()

    # Checking user choice
    while True:
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


# Showing movies list
def movies_list(movies):
    print(f"{len(movies)} movies in total")
    for movie,data in movies.items():
        print(f"{movie} ({data["year"]}): {data["rating"]}")


# Add movie
def add_movie(movies):
    try:
        movie_name = input("Enter movie name: ")

        final_url = MOVIES_URL+movie_name
        response = requests.get(final_url)
        res = response.json()
        while res.get("Response") == "False":
            print(res["Error"]+"\n")
            movie_name = input("Enter movie name or press q to go back to the main menu: ")
            if movie_name == "q":
                print("\n")
                user_choice()
            final_url = MOVIES_URL + movie_name
            response = requests.get(final_url)
            res = response.json()
        if res["Title"] in movies:
            storage.list_movies()
            print("Movie already exists please use the (List movies command to see the available movies)")
        else:
            storage.add_movie(res["Title"],res["Year"], res["imdbRating"],res["Poster"])
        print(f"\nMovie {res["Title"]} has been added")
    except ValueError as value_error:
        print(f"This can not be a movie name {value_error}")


# Update movie rating
def update_movie(movies):
    movie_name = input("Enter movie name: ")
    while movie_name not in movies:
        movie_name = input(
            f"Movie name {movie_name} does not exist please enter a valid movie name or press q to exit: ")
        if movie_name == "q":
            print("\n")
            user_choice()
    movie_rating = float(input("Enter new movie rating (0-10): "))
    while 0.0 > movie_rating or movie_rating > 10.0:
        movie_rating = float(input(f"Rating {movie_rating} is invalid please enter another rating: "))
    movies[movie_name]["movie_rating"] = movie_rating
    # ms.update_movie(movie_name, movie_rating)
    print(f"Movie {movie_name} has been updated")


# Delete a movie
def del_movie(movies):
    movie_name = input("Enter movie name: ")
    while movie_name not in movies:
        movie_name = input(f"Movie {movie_name} does not exist please enter a valid movie name or press q to exit:")
        if movie_name == "q":
            print("\n")
            user_choice()
    storage.delete_movie(movie_name)
    print(f"Movie {movie_name} has been deleted")


# Showing movie stats
def movies_stats(movies):
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
    rand_value = rnd.sample(list(movies.items()), 1)
    print(
        f"Your movie for tonight: {rand_value[0][0]} ({rand_value[0][1]["year"]}), it's rated {rand_value[0][1]["rating"]}")


# Search a movie
def search_movie(movies):
    query = input("Enter part of movie name: ")
    for movie, value in movies.items():
        # if query in movie:
        if fuzz.partial_ratio(query.lower(), movie.lower()) > 60:
            print(movie, value["rating"])


# Sort movies in descending order by rating
def sorted_by_rating(movies):
    value = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    print("\n\n")
    for movie, rating in value:
        print(movie, rating["rating"])


def generate_movie(movies):
    movie_html_data = load_html_data('_static/index_template.html')
    output = ''  # define an empty string
    for movie,value in movies.items():
        output += serialize_movie(movie,value)

    new_html_data = movie_html_data.replace('__TEMPLATE_MOVIE_GRID__', output)
    save_to_html(new_html_data, '_static/movies.html')
    print("Website was generated successfully.\n")


# Our main function where our movies app first launch
def main():
    title = "*" * 7 + " Welcome to my movies app " + "*" * 7
    print(title, end="\n\n")
    # Your code here
    user_choice()


if __name__ == "__main__":
    main()
