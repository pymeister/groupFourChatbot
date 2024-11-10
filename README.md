# Chatbot: Simple Medical Recommendation Bot

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Basic Commands

## Running the Application

### Install Postgresql

```bash
brew install postgresql@15 # for Mac

```
```bash
apt install postgresql # for Linux

```
```bash
sudo pacman -S postgresql # for Arch Linux

```
[PostgreSQL Download](https://www.postgresql.org/download/) # for Others

### Create Database Chatbot

Open postgresql command line  tool
```bash
psql -U postgres
```
Create database
```bash
postgres=# CREATE DATABASE chatbot;
```
Connect database
```bash
postgres=# \c chatbot
```
Exit postgresql command line tool
```bash
postgres=# \q
```
### Opening and Closing the Python Environment

To open the Python Environment:

```bash
source env/bin/activate  # for Linux/Mac
```
```bash
source .\venv\Script\activate  # for Windows
```

To close the Python Environment:

```bash
deactivate
```

### Installing all Python Requirements

Once the Python environment is open run:
```bash
pip install -r requirements/local.txt

```
This install Django and all the required files need to run the program.

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
### Setting Up Your Users

#### Creating a Normal User Account

To create a normal user account, simply go to the Sign Up page and fill out the form. Once you submit it, you will see a "Verify Your E-mail Address" page. Open your console to see a simulated email verification message. Copy the link into your browser, and now your user's email should be verified and ready to use.

#### Creating a Superuser Account

To create a superuser account, run this command:

```bash
$ python manage.py createsuperuser
```


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

### Logging into the Admin Backend

To log into the admin backend, go to `http://localhost:8000/admin` in your browser and enter the username and password you set up when creating a superuser account.
