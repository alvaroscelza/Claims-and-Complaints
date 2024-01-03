# Claims and Complaints

This project is a Django application that allows users to create claims and complaints about different companies.

## Technology Stack

- Python 3.11
- Django 4
- PostgreSQL 15

## Installation and running

- Create virtual environment. Example: `virtualenv venv`
- Enter environment: Example: `venv\Scripts\activate`
- Install requirements: `pip install -r requirements.dev.txt`
- Install pre-commit hooks feature: `pre-commit install`
- Create `.env` file at project root. File .env-example is provided as a guide of this file's content.
- Generate migration files: `python manage.py makemigrations`
- Run migrations: `python manage.py migrate`
- Create superuser: `python manage.py createsuperuser`
- Run using `python manage.py runserver`
- To see the documentation diagrams you require [Graphviz](https://graphviz.org/).
- To generate dependencies graph
  - All dependencies: `pydeps applications --cluster --keep-target-cluster --rmprefix applications. --reverse`
  - Only circular dependencies: `pydeps applications --show-cycles --reverse`
  - Only
    Core: `pydeps applications --cluster --keep-target-cluster --rmprefix applications. --reverse --only applications.core`

## Testing

- Run the tests with `python manage.py test`
- Get test coverage with:
  - `coverage run --source='.' manage.py test`
  - `coverage report --skip-covered --show-missing`

## Re-generate translations

- Install GNU gettext tools: https://www.gnu.org/software/gettext/
- Run the following command to generate django.po file:
  `django-admin makemessages -l es --all --ignore venv --no-location`
- Once all the translations are made, run the command: `django-admin compilemessages`
