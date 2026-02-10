def save_to_html(html_data,file_path):
    with open(file_path, "w") as handle:
        handle.write(html_data)


def load_html_data(file_path):
  """ Loads a JSON file """
  with open(file_path, "r") as handle:
    return handle.read()

def serialize_movie(movie_name,movie_values):
    output_obj = ''  # define an empty string
    output_obj += '<li class="movie-grid li">'
    output_obj += '<div class="movie">'
    output_obj += f'<img class="movie-poster" src="{movie_values["poster"]}">\n'
    output_obj += f'<div class="movie-title">{movie_name}</div>\n'
    output_obj += f'<div class="movie-year">{movie_values["year"]}</div>\n'
    output_obj += f'</div>'
    output_obj += '</li>'
    return output_obj