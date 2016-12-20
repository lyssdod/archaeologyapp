## Archaeology database

This repository holds the source for a website that implements a handy database of archaeological sites across the world. 

### Demo
You can reach the site at http://archdb.tk/ and log in using the following credentials:
username: `demo`, password: `demopass`

### Running

#### NOTE
Code has been updated to run on Heroku, so if you have account there you can
skip following lines and just deploy app there.

#### Configuration
By default app uses Django's `DEBUG` set to `True` and uses sqlite database
backend. If you need to change this behaviour, you need to set few environment
variables:

* `DEBUG` to anything except `1`, `TRUE` or `Y`
* `DATABASE_URL` to full database URI (see https://github.com/kennethreitz/dj-database-url for more details)

Keep in mind that `DATABASE_URL` will be used only with disabled `DEBUG`. You can also set logfile
name and allowed hosts with `LOGFILE` and `ALLOWED` env vars.

#### Steps
0. Setup a virtual environment: `virtualenv venv && source venv/bin/activate`
1. Install everything you need: `pip install -r requirements.txt`
3. Make migrations and migrate: `python manage.py makemigrations archapp && python manage.py migrate`
4. Create default filters: `python manage.py loaddata archapp/fixtures/filters.json`
5. Create administrator: `python manage.py createsuperuser`
6. Go! `python manage.py runserver`

If you really like production environments, you probably should consider deployment using `nginx` and `gunicorn`:
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-14-04
