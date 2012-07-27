# smartcoops

We bring a marketplace and mobile banking to agricultural coops. Check out the [wiki to learn more](http://github.com/dannycastonguay/smartcoops/wiki)

## Manifest

There are currently two parts to this project. One is a Django web app that deploys to Heroku, and the other is a Python command line simulator for farmer interactions with the yet to be built SMS server.

# SMS Simulator Installation

1. Install Python 2.5 or above (not Python 3.X unfortunately, since django does not support 3.X yet)
1. Install [git](http://git-scm.com/downloads)
1. Go to the folder where you want to code (in my examples, I type `cd ~/antportal/`)
1. `git clone git@github.com:dannycastonguay/smartcoops.git`

## Running the Simulator

1. `python ~/antportal/smartcoops/pilot/smsSimulator.py`

## Django app on Heroku Installation

2. `curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py`
1. `python virtualenv.py scenv`  
1. `source ~/antportal/scenv/bin/activate`
1. `pip install django`
1. `pip install dj-database-url`
1. `pip install django-extensions`
1. Follow instructions from the [dev center of Heroku](https://devcenter.heroku.com/articles/django)
1. (Under macos) You might run into trouble with the installation of postgre, if so this [article might help you](http://stackoverflow.com/questions/846383/problem-installing-pyscopg2-on-mac-os-x)
1. Add your ssh key to heroku `heroku keys:add` 
1. `git remote add heroku git@heroku.com:tranquil-ocean-3872.git`

### Run the django app locally

1. `python ~/antportal/smartcoops/django manage.py syncdb`
1. `python ~/antportal/smartcoops/django manage.py runserver`
1. Go to `127.0.0.1:8000` or `127.0.0.1:8000` 

### Run the django app on heroku

1. Check that the django app runs locally
1. From the root of the directory, `git add` the files you have modified 
1. `git commit -m "some meaningful commit message"`
1. `git push` so your changes go to GitHub
1. `git push heroku master`
1. `heroku run python manage.py syncdb`
1. Check that it works by visiting the [home page](http://tranquil-ocean-3872.heroku.com) and the [admin page](http://tranquil-ocean-3872.heroku.com/admin) on Heroku

## Copyright

For the time being, all rights reserved to [AntPortal Corp of Canada](http://www.antportal.com).

