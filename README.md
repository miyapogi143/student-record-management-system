# Campus Records

A Django student record management system for a school office or classroom demo. It includes student profiles, a course catalog, term enrollments, grade tracking, search, CSV export, staff sign-in, and Django Admin.

## Stack

- Django 5.x
- PostgreSQL on Render (configured through `DATABASE_URL`)
- SQLite by default for local development
- Gunicorn and WhiteNoise for production serving

## Run locally on Windows

Install Python 3.12, open PowerShell in this project folder, and run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/> and sign in with the staff account you created. If PowerShell blocks virtual-environment activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and activate again.

The sample-data command creates 8 example students, 6 courses, and term enrollment/grade records. It is safe to run more than once. The sample email addresses use the reserved `example.com` domain, and phone numbers are placeholders; the records are fictional demo data.

## Deploy to Render

This project includes a Render Blueprint in `render.yaml`. To deploy:

1. Put this project folder in a Git repository and push it to GitHub or another Git provider supported by Render.
2. In Render, choose **New → Blueprint**, connect the repository, and confirm the resources from `render.yaml`.
3. Render provisions a Django web service and PostgreSQL database. The Blueprint enables auto-deploys for new commits.
4. Once deployment completes, open the web-service URL and use **Render Shell** to create your own staff account:

   ```sh
   python manage.py createsuperuser
   ```

Render runs `build.sh` during deploy. It applies database migrations, loads the example records, and collects static assets. The app reads the PostgreSQL connection from Render's `DATABASE_URL`; do not put production credentials in the repository. The web service is configured to run with Gunicorn and to use HTTPS-aware Django settings.

The Blueprint uses Render's free-plan settings as a starting point. Free database availability, lifetime, and persistence limits can change; choose a suitable paid database and configure backups before storing important information.

## Main workflows

- Dashboard with student, active-student, course, and enrollment totals
- Searchable student directory, student profiles, and enrollment history
- Student and course create/edit/delete workflows
- Course registration by school year and semester
- Prelim, midterm, and final grades with a calculated average
- Student-record CSV export
- Django Admin for staff administration
- Responsive interface for desktop and mobile

## Data and access

- Local development uses `db.sqlite3` unless `DATABASE_URL` is set.
- Production uses PostgreSQL, configured by the Render Blueprint.
- Staff accounts are created by an administrator; there is no public registration or hard-coded demo password.
- Never use the example data for real student information. Before institutional use, add appropriate role-based access, audit logging, privacy/retention policies, operational monitoring, and database backups.

## Project layout

```text
manage.py
render.yaml
build.sh
requirements.txt
student_records/           # Django settings, URLs, and WSGI
records/                   # Models, forms, views, migrations, and seed command
templates/                 # Application and sign-in pages
static/css/                # Application styles
```
