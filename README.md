# 🏝️ West Lombok Tourism Website

A modern tourism destination website for West Lombok, built with Django and Tailwind CSS.

![Django](https://img.shields.io/badge/Django-5.1.3-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Tailwind](https://img.shields.io/badge/Tailwind-CSS-cyan)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📖 About

This website showcases the beautiful tourism destinations of West Lombok (Lombok Barat), Indonesia. It features destination browsing, category filtering, search functionality, and a unique "Surprise Me" feature that randomly suggests destinations.

## ✨ Features

- **Destination Management** - Browse, search, and filter destinations
- **Category System** - Organized by tourism types (Beach, Nature, Culture, etc.)
- **Search & Filter** - Find destinations by keyword or category
- **Surprise Me** - Random destination suggestion with animated reveal
- **Admin Dashboard** - Modern admin panel with django-unfold
- **Responsive Design** - Mobile-first, fully responsive UI
- **View Counter** - Track popular destinations

## 🛠️ Technology Stack

| Layer    | Technology                       |
| -------- | -------------------------------- |
| Backend  | Django 5.1.3                     |
| Frontend | Tailwind CSS                     |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Admin    | django-unfold                    |
| Icons    | Google Material Icons            |

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Node.js (for Tailwind CSS)

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/PROJECT-PKL.git
   cd PROJECT-PKL
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**

   ```bash
   cp .env.example .env
   # Edit .env and set your SECRET_KEY
   ```

5. **Run migrations**

   ```bash
   python manage.py migrate
   ```

6. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**

   ```bash
   python manage.py runserver
   ```

8. **Visit the website**
   - Frontend: http://127.0.0.1:8000
   - Admin: http://127.0.0.1:8000/admin

## 📁 Project Structure

```
PROJECT-PKL/
├── apps/
│   ├── base/           # Home & About pages
│   └── core/           # Destinations & Categories
├── config/             # Django settings
├── media/              # Uploaded images
├── static/             # Static assets
├── templates/          # HTML templates
│   ├── base/
│   ├── core/
│   └── components/
├── manage.py
└── requirements.txt
```

## 🔧 Configuration

Key settings can be configured via environment variables:

| Variable               | Description           | Default   |
| ---------------------- | --------------------- | --------- |
| `DJANGO_SECRET_KEY`    | Secret key for Django | (dev key) |
| `DJANGO_DEBUG`         | Enable debug mode     | True      |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hosts | localhost |

## 📸 Screenshots

_(Add screenshots of your application here)_

## 📄 License

This project is created for educational purposes (PKL/Internship) at DISKOMINFO Lombok Barat.

## 👤 Author

**Your Name**

- Institution: [Your Institution]
- Supervised by: DISKOMINFO Lombok Barat

---

Made with ❤️ in West Lombok, Indonesia
