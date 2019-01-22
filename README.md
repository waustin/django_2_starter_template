Django Starter Template
===========================

A Django 2.0+ starter project template I use as a starting point for content based sites.
Includes a number of bundled apps that can be customized to a site's needs


### Features
* Multiple settings files for different environments (dev, production, etc).
* A base settings file for settings common across environments
* Relative paths in the settings file
* django-dotenv support in manage.py
* Starter Base Template file
* Starter SASS / Compass styles
* An app directory to keep custom django apps organized and out of the
  project's base directory
* A development Procfile to launch the django dev server and compass
* dj-database-url to make it easier to move DB configuration into a ENV var
* Common Bundled Applications
* A a basic fabric file to help deployment to WebFaction
* A requirements template of basic apps to install

* Rename env to .env in root to specify the DATABASE_URL and DJANGO_SETTINGS_MODULE.
* _Note: .env files should not be checked into your git repo_


### Bundled Applications
* Pages - multi-level page application with ability to override page templates
* Blog - simple blogging application
* Promotions - create banner ads to show in templates
* Text Block - Admin manageable bits of text
* Overrides for django-sitetree to make it's admin more user friendly
