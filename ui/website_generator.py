

def save_to_html(html_data,file_path):
    """
        Writes a string of HTML data to a specified file path.

        Args:
            html_data (str): The complete HTML content to be saved.
            file_path (str): The system path where the .html file should be created.
        """
    with open(file_path, "w") as handle:
        handle.write(html_data)


def load_html_data(file_path):
  """
    Reads the content of an HTML template file.

    Args:
        file_path (str): The path to the HTML template file.

    Returns:
        str: The raw string content of the file.
    """
  with open(file_path, "r") as handle:
    return handle.read()


def serialize_movie(movie_name,movie_values):
    """
        Converts a single movie's data into an HTML list item (<li>) string.

        This function takes movie metadata and wraps it in specific HTML tags
        and classes to match the CSS grid styling of the final website.

        Args:
            movie_name (str): The title of the movie.
            movie_values (dict): A dictionary containing 'poster' (URL) and 'year'.

        Returns:
            str: A formatted HTML string representing one movie card.
        """
    # output_obj = ''  # define an empty string
    # output_obj += '<li class="movie-grid li">'
    # output_obj += '<div class="movie">'
    # output_obj += f'<img class="movie-poster" src="{movie_values["poster"]}">\n'
    # output_obj += f'<div class="movie-title">{movie_name}</div>\n'
    # output_obj += f'<div class="movie-year">{movie_values["year"]}</div>\n'
    # output_obj += f'</div>'
    # output_obj += '</li>'
    return f"""
    <li class="movie-grid li">
        <div class="movie">
            <img class="movie-poster" src="{movie_values['poster']}">
            <div class="movie-title">{movie_name}</div>
            <div class="movie-year">{movie_values['year']}</div>
        </div>
    </li>
    """
