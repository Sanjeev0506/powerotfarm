Power OT Farms — backend

Minimal Django backend for contact submissions, orders and payments (skeleton).

This project is intentionally small and designed to be hosted on a server (no Docker). Use the `.env` file to configure MySQL and SMTP.

Quick local setup (Windows / PowerShell):

1. Create a virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and adjust values. If you leave MySQL values empty, sqlite will be used.

3. Run migrations and start the dev server:

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

4. Contact endpoint:
   - POST to `/api/contact/submit/` with form fields `name,email,phone,subject,message` (Content-Type: application/x-www-form-urlencoded or multipart/form-data)

Production notes:
- Use a WSGI server like gunicorn or daphne for ASGI. Configure Nginx as a reverse proxy.
- Ensure `DJANGO_DEBUG=False` and `DJANGO_ALLOWED_HOSTS` set to your host.
- Set SMTP variables in `.env` to enable email notifications.
