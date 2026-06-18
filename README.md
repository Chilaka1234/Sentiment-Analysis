# Sentiment App

A simple Django sentiment analysis web app that classifies user reviews as `positive`, `negative`, or `neutral` using a Naïve Bayes-style review classifier and the provided `yelp_labelled.csv` dataset.

## Project Structure

- `manage.py` - Django management script.
- `sentiment_app/` - Django project settings and URL configuration.
- `reviews/` - Django app containing views, templates, and sentiment logic.
- `reviews/templates/` - HTML pages for the review form and result display.
- `yelp_labelled.csv` - labelled dataset used for sentiment classification.
- `Sentiment.py` - standalone script for processing the dataset manually.
- `db.sqlite3` - Django SQLite database file.

## Prerequisites

- Python 3.11+ or another supported Python 3 version.
- `pip` installed.
- Django installed in your environment.

## Installation

1. Open a terminal in the project root.
2. Create a virtual environment (recommended):

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install Django:

   ```powershell
   pip install django
   ```

## Run the App

From the project root, start the Django development server:

```powershell
python manage.py runserver
```

Open your browser at:

```
http://127.0.0.1:8000/
```

## Usage

- Enter a review on the homepage form.
- Submit to see the predicted sentiment and review details.

## Notes

- Sentiment prediction uses the `yelp_labelled.csv` dataset.
- The main logic is in `reviews/views.py`.
- The app currently runs in Django debug mode and is intended for local development.

## Troubleshooting

- If Django is not installed, install it with `pip install django`.
- If you encounter encoding issues loading the CSV, ensure the file is in UTF-8 format.

## Optional

- To reset the database or create migrations, use:

  ```powershell
  python manage.py migrate
  ```
