## Archaeology database

This repository holds the source for a website that implements a handy database of archaeological sites across the world. 

### Demo
You can reach the site at http://archdb.tk/en/archapp and log in using the following credentials:
username: `demo`, password: `demopass`

### Running
0. Setup a virtual environment: `virtualenv venv && source venv/bin/activate`
1. Install everything you need: `pip install -r requirements.txt`
2. (not necessary) Create config file named `settings.ini` in the root repository folder:
```
[archapp]
# Defaults, app will use sqlite backend. Also enables Django debug.
debug = true 

# if you feel production ready, you can set up a Postgresql database 
# and fill the lines below. they will be ignored if debug == true.
dbname = ...
dbuser = ...
dbpass = ...
```
3. Make migrations and migrate: `python manage.py makemigrations archapp && python manage.py migrate`
4. Create default filters: `python manage.py loaddata archapp/fixtures/filters.json`
5. Create administrator: `python manage.py createsuperuser`
6. Go! `python manage.py runserver`

If you really like production environments, you probably should consider deployment using `nginx` and `gunicorn`:
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-14-04
