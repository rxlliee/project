# Fourfolio Portfolio Website

This project uses Django for the backend and keeps the existing portfolio page as
the frontend. Portfolio owners and content can be managed through Django admin.

## Quick start

1. Create and activate a virtual environment:

```bash
cd Website
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create database tables and an admin account:

```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Run the server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the portfolio frontend and
`http://127.0.0.1:8000/admin/` for content management.

## API endpoints

- `GET /api/profiles/` lists active portfolio profiles.
- `GET /api/profiles/<slug>/` returns a complete profile payload.
- `POST /api/profiles/<slug>/contact/` accepts `sender_name`, `sender_email`,
  `subject`, and `message` as JSON and stores a contact message.

For production, set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=False`,
`DJANGO_ALLOWED_HOSTS`, and the PostgreSQL variables from `.env.example`, then
run `python manage.py collectstatic` and serve with Gunicorn.
