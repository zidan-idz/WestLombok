<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=rect&color=0:3776AB,100:06B6D4&height=120&section=header&text=West%20Lombok&fontSize=60&fontColor=ffffff&animation=scaleIn" width="100%"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/TailwindCSS-3.4-06B6D4?logo=tailwindcss&logoColor=white" alt="TailwindCSS">
  <img src="https://img.shields.io/badge/Anime.js-3.2.1-FF69B4?logo=javascript&logoColor=white" alt="Anime.js">
</p>

---

A tourism destination information website for West Lombok Regency. Provides a complete catalog of tourist attractions categorized by type and district.

## Features

- Complete destination catalog with photos and detailed descriptions
- Filter by category and district
- "Surprise Me" feature for random destination recommendations
- Responsive mobile-friendly design
- Modern admin panel with Django Unfold

## Screenshot

![Screenshot Home](docs/home.png)

> **See more screenshots:** [Click here](./docs/)

## Prerequisites

Make sure you have installed:

- Python 3.10+
- Node.js 18+ (for Tailwind CSS)
- Git

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/USERNAME/west-lombok.git
cd west-lombok
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

**Activate (Windows):**

```bash
venv\Scripts\activate
```

**Activate (Linux/Mac):**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Tailwind

```bash
python manage.py tailwind install
```

### 5. Create Environment File

```bash
cp .env.example .env
```

### 6. Generate Secret Key

Generate a new SECRET_KEY for your project:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it into your `.env` file as `DJANGO_SECRET_KEY`.

### 7. Run Database Migration

```bash
python manage.py migrate
```

### 8. Create Admin Account

```bash
python manage.py createsuperuser
```

### 9. (Optional) Load Dummy Data

```bash
python manage.py loaddata fixtures/initial_data.json
```

### 10. Run Development Server

```bash
python manage.py runserver
```

Open your browser and access:

- Website: http://127.0.0.1:8000/
- Admin Panel: http://127.0.0.1:8000/admin/

## Environment Variables

| Variable               | Description                    | Example                       |
| ---------------------- | ------------------------------ | ----------------------------- |
| `DJANGO_SECRET_KEY`    | Secret key for Django security | `your-secret-key-here`        |
| `DJANGO_DEBUG`         | Debug mode (True/False)        | `True`                        |
| `DJANGO_ALLOWED_HOSTS` | List of allowed hosts          | `example.com,www.example.com` |

## Production Database Configuration

By default, this project uses SQLite for development. For production, it is recommended to use MySQL or PostgreSQL.

### MySQL

1. Install driver:

```bash
pip install mysqlclient
```

2. Edit `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database_name',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### PostgreSQL

1. Install driver:

```bash
pip install psycopg2-binary
```

2. Edit `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'database_name',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

After changing the database configuration, run migration:

```bash
python manage.py migrate
```

## Troubleshooting

### Tailwind not working

Make sure Node.js is installed:

```bash
node --version
```

If not installed, download from [nodejs.org](https://nodejs.org/)

### Error "No module named 'apps'"

Make sure the file `apps/__init__.py` exists:

```bash
# Windows
type nul > apps\__init__.py

# Linux/Mac
touch apps/__init__.py
```

### Static files not showing

Run collectstatic:

```bash
python manage.py collectstatic
```

## License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/USERNAME">Zidan IDz</a>
</p>

<p align="center">
  If you find this project useful, give it a ⭐
</p>
