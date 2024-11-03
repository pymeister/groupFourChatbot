# Chatbot: Simple Medical Recommendation Bot

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
License: MIT

## Basic Commands

### Setting Up Your Users

#### Creating a Normal User Account

To create a normal user account, simply go to the Sign Up page and fill out the form. Once you submit it, you will see a "Verify Your E-mail Address" page. Open your console to see a simulated email verification message. Copy the link into your browser, and now your user's email should be verified and ready to use.

#### Creating a Superuser Account

To create a superuser account, run this command:

```bash
$ python manage.py createsuperuser
```

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type Checks

To check your code for type errors, run `mypy`:

```bash
$ mypy chatbot
```

### Test Coverage

To run your tests, first run the test command and then generate an HTML coverage report:

```bash
# Run tests with pytest
$ pytest

# Check test coverage
$ coverage run -m pytest
# Generate HTML coverage report
$ coverage html
# Open HTML coverage report
$ open htmlcov/index.html
```

## Running the Application

### Opening and Closing the Python Environment

To open the Python environment:

```bash
source env/bin/activate  # for Linux/Mac
```

To close the Python environment:

```bash
deactivate
```

### Running Basic Commands

#### Running the Server

Run the server with:

```bash
$ python manage.py runserver
```

Open your browser at `http://localhost:8000` to access the chatbot.

#### Running Static Files

Run static files with:

```bash
$ python manage.py collectstatic
```

#### Creating Migrations

Create migrations with:

```bash
$ python manage.py makemigrations
```

Apply migrations with:

```bash
$ python manage.py migrate
```

### Logging into the Admin Backend

To log into the admin backend, go to `http://localhost:8000/admin` in your browser and enter the username and password you set up when creating a superuser account.

Note: This documentation assumes that you have installed Django, Cookiecutter-Django, and Ruff. If you need help installing these tools, please let me know!
