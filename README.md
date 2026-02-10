# Movie Management System

A comprehensive Python-based command-line application for managing a personal movie database. This project allows users to track their favorite movies, fetch details from the OMDB API, store data in a SQLite database using SQLAlchemy, and generate a visually appealing static website to showcase their collection.

## Features

- **Movie Management**: Add, delete, and update movie ratings.
- **OMDB Integration**: Automatically fetch movie details (Year, Rating, Poster) using the OMDB API.
- **Database Storage**: Persistent storage using SQLite and SQLAlchemy.
- **Statistics**: View database stats including average rating, median rating, and best/worst movies.
- **Search & Discovery**: 
  - Fuzzy search for movies (powered by `fuzzywuzzy`).
  - Random movie suggestions for your next watch.
  - Sort movies by rating.
- **Website Generation**: Generate a static HTML website (`movies.html`) from your database using a customizable template.

## Project Structure

```text
python_movie_project/
├── data/
│   └── movies.db              # SQLite database file
├── storage/
│   └── movie_storage_sql.py   # Database operations using SQLAlchemy
├── ui/
│   └── website_generator.py   # Logic for HTML generation
├── _static/
│   ├── index_template.html    # HTML template for the website
│   ├── style.css              # CSS for the generated website
│   └── movies.html            # Generated output website
├── movies.py                  # Main entry point of the application
├── requirements.txt           # Project dependencies
└── .env                       # Environment variables (API Key)
```

## Installation

1. **Clone the repository** (or extract the project files).
2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

This project requires an **OMDB API Key** to fetch movie data.

1. Get a free API key from [OMDB API](https://www.omdbapi.com/apikey.aspx).
2. Create a `.env` file in the root directory.
3. Add your API key to the `.env` file:
   ```text
   API_KEY=your_api_key_here
   ```

## Usage

Run the main script to start the application:

```bash
python movies.py
```

### Menu Options:
- `0. Exit`: Close the application.
- `1. List movies`: Show all movies in the database.
- `2. Add movie`: Fetch and add a new movie from OMDB.
- `3. Delete movie`: Remove a movie from the database.
- `4. Update movie`: Change a movie's rating.
- `5. Stats`: Display database statistics.
- `6. Random movie`: Get a random movie suggestion.
- `7. Search movie`: Search for a movie using fuzzy matching.
- `8. Movies sorted by rating`: List movies from highest to lowest rating.
- `9. Generate movie website`: Create `_static/movies.html` to view your collection in a browser.

## Technologies Used

- **Python 3.13**
- **SQLAlchemy**: For database ORM and management.
- **Requests**: To interact with the OMDB API.
- **FuzzyWuzzy**: For flexible string matching in searches.
- **Python-Dotenv**: For managing environment variables.
- **HTML/CSS**: For the generated movie website.

## License

This project is open-source and available for personal use.
