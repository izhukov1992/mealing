# mealing

## Local Installation

* `sudo apt-get install nodejs`
* `sudo apt-get install npm`
* `sudo npm install -g bower`
* `git clone https://github.com/izhukov1992/ct.git`
* remove psycopg2 and dj-database-url from requirements.txt.
* remove lines from mealing/settings.py:
  * import dj_database_url
  * DATABASES['default'] =  dj_database_url.config()
* `bower install` or `sudo bower install --allow-root`
* `python pip install -r requirements.txt`
* `python manage.py migrate`
* `python manage.py createsuperuser`
* `python manage.py runserver`

## Heroku Installation

* https://dashboard.heroku.com/apps -> New -> create new app.
* https://dashboard.heroku.com/apps/<app_name>/resources -> Add-ons enter and add Heroku Postgres.
* https://dashboard.heroku.com/apps/<app_name>/settings -> Buildpacks -> Add buildpack -> Python -> Save changes.
* https://dashboard.heroku.com/apps/<app_name>/settings -> Buildpacks -> Add buildpack -> nodejs -> Save changes.
* https://dashboard.heroku.com/apps/<app_name>/deploy -> Deployment method -> GitHub. Enter name, enter repo name, press Search, press connect, choose branch, press Deploy branch, wait for deploying.
* https://<app_name>.herokuapp.com
* `wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh`
* `heroku login`
* `heroku run migrate`
* `heroku run python manage.py migrate`
* `heroku run python manage.py createsuperuser`

## First step
* /api/v1/reporter/ -> Post new reporter for superuser.

## Testing
* `python manage.py test`

## App references

* /#!/auth
* /#!/
* /#!/manager

## API references

* /api/v1/
* /api/v1/auth/
* /api/v1/user/
* /api/v1/reporter/
* /api/v1/meal/
* /api/v1/user/%id%/
* /api/v1/reporter/%id%/
* /api/v1/meal/%id%/