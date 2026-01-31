# Backend Setup Guide - HRMS Lite

Complete guide for setting up the Django backend locally.

## Prerequisites

- Python 3.11 or higher
- PostgreSQL 14 or higher
- pip (Python package manager)
- virtualenv (recommended)

## Step-by-Step Setup

### 1. PostgreSQL Database Setup

#### On Windows

1. **Install PostgreSQL:**
   - Download from: https://www.postgresql.org/download/windows/

2. **Create Database:**
   ```bash
   # Open SQL Shell (psql) from Start Menu
   # Press Enter for default values, then enter your password
   
   CREATE DATABASE hrms_db;
   CREATE USER hrms_user WITH PASSWORD 'your_password';
   ALTER ROLE hrms_user SET client_encoding TO 'utf8';
   ALTER ROLE hrms_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE hrms_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE hrms_db TO hrms_user;
   ```

### 2. Python Virtual Environment

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### 3. Install Dependencies

```bash
# Make sure virtual environment is activated
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependencies include:**
- Django 5.0.1
- djangorestframework 3.14.0
- psycopg2-binary 2.9.9 (PostgreSQL adapter)
- python-dotenv 1.0.0
- django-cors-headers 4.3.1
- whitenoise 6.6.0 (static files)
- gunicorn 21.2.0 (production server)

### 4. Environment Configuration

**Edit .env:**
```env
SECRET_KEY=django-insecure-dev-key-CHANGE-THIS
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=hrms_db
DB_USER=hrms_user
DB_PASSWORD=your_password  # <-- Change this
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### 5. Database Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

```

### 6. Create Superuser (Optional)

```bash
python manage.py createsuperuser

```

### 7. Run Development Server

```bash
python manage.py runserver

# Server will start at: http://127.0.0.1:8000/
# Admin panel at: http://127.0.0.1:8000/admin/
```
