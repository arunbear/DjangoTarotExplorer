# Django Tarot Explorer

A static site generator for exploring Tarot cards, built with Django and django-distill.

## Prerequisites

- Python 3.8+
- pip

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd DjangoTarotExplorer
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Development

### Run development server
```bash
python manage.py runserver
```

The site will be available at `http://127.0.0.1:8000/`

## Building the Static Site

Start the development server as above, then run

### Build to local directory
```bash
cd /path/to/static/site
wget --recursive --no-host-directories http://127.0.0.1:8000
```

The static site will be generated in this directory.

## Project Structure

- `gallery/` - Main Django app containing Tarot card models and views
- `tarotexplorer/` - Django project settings
- `public/` - Generated static site (after build)
- `static_root/` - Collected static files
- `templates/` - Global templates

## Features

- Browse all Tarot cards
- View cards by suite (Wands, Cups, Swords, Coins)
- View Trump cards
- Interactive card dealing feature
- Responsive design

## License

This project is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0).

You are free to:
- Share — copy and redistribute the material in any medium or format
- Adapt — remix, transform, and build upon the material

Under the following terms:
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made
- ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original

See [LICENSE](LICENSE) file for details or visit https://creativecommons.org/licenses/by-sa/4.0/
