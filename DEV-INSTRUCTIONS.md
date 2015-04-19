# ling-sleuth
Learn a little linguistics
## How to run the app
## Install `virtualenv` for python 2.7.x

`pip install virtualenv --python=python2.7`

## Create a virtual environment

From the project directory, `virtualenv venv`
## Activate the virtual environment
### 1) Activating the python virtual environment  

From the project directory, `source venv/bin/activate`

### 2) Installing the project dependencies

After activating the vm, make sure you have all of the necessary dependencies installed.  Simply type:  
`pip install -r requirements.txt`

## Setting up the database

We're using `Flask-Migrate` to handle changes to the database models.

### First-time setup of database

`python manage.py db init`

This will create a database

### Handling migrations

`python manage.py db migrate`

which creates the migration script, and

`python manage.py db upgrade`

which updates the database with the new migration script.

### Add modules

Specify a module to be added to the database and its fields by adding a line to 
mod_list.csv, in the /app directory. Any fields you do not currently wish to add information
for a given field, simply tab to the next field.

### Initialize user ranks, levels, and modules

If the database needs to be recreated, and these values reinitialized, run

`python manage.py reboot`

which will automatically load in the specified ranks, levels, and modules.

### Learn more

`python manage.py db --help`

## Running the web app locally

  1. From the project directory, type:  
`./run.py`  
  2. In your browser, navigate to [`http://localhost:5000`](http://localhost:5000)

## Adding dependencies

Install a new package:  

`pip install <some package name here>`

Update `requirements.txt`:  
`pip freeze > requirements.txt`

Be careful not to add unnecessary dependencies to `requirements.txt`

## Exiting the virtual environment

`deactivate`
