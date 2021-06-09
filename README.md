# django-ent
[![Python 3.9](https://img.shields.io/badge/python-3.7|3.8|3.9-blue.svg)](https://www.python.org/downloads/release/python-390/) 
[![Django 2.2](https://img.shields.io/badge/django-2.2-blue.svg)](https://docs.djangoproject.com/en/2.2/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)  
Handle CAS login via sso for french ENT (Etablissements Numériques de Travail) like 
ENT Hauts-de-France (HDF) or Occitanie (OCCITANIE) or Occitanie lycée agricole (OCCITANIEAGR).

## Installation
Install with [pip](https://pip.pypa.io/en/stable/):
```shell
pip install -e git://github.com/briefmnews/django-ent.git@main#egg=django_ent
```

## Setup
In order to make `django-ent` works, you'll need to follow the steps below.

### Settings
First you need to add the following configuration to your settings:
```python
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',

    'django_ent',
    ...
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    'django_ent.middleware.CASMiddleware',
    ...
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    
    'django_ent.backends.CASBackend',
    ...
)
```

### Migrations
Next, you need to run the migrations in order to update your database schema.
```shell
python manage.py migrate
```

### Mandatory settings
Here is the list of all the mandatory settings:
```python
ENT_HDF_BASE_URL
ENT_OCCITANIE_BASE_URL
ENT_OCCITANIEAGR_BASE_URL
ENT_QUERY_STRING_TRIGGER
```

### Optional settings - Default redirection
You can set a default path redirection for inactive user by adding this line to 
your settings:
```python
ENT_INACTIVE_USER_REDIRECT = '/{mycustompath}/'
```
`ENT_INACTIVE_USER_REDIRECT` is used if an inactive user with a valid ticket
tries to login.
If `ENT_INACTIVE_USER_REDIRECT` is not set in the settings, it will take
the root path (i.e. `/`) as default value.


## How to use ?
Once your all set up, when a request to your app is made with the query string 
`sso_id=<unique_uai>`, the `CASMiddleware` catches the request and start the login process. 
Here is an example of a request url to start the login process:
```http request
https://www.exemple.com/?sso_id=9990075c

## Tests
Testing is managed by `pytest`. Required package for testing can be installed with:
```shell
pip install -r test_requirements.txt
```
To run testing locally:
```shell
pytest
```

## Credits
- [python-cas](https://github.com/python-cas/python-cas)
- [django-cas-ng](https://github.com/mingchen/django-cas-ng)

## References
- [CAS protocol](https://www.apereo.org/projects/cas)
