# Simple Chat API

Simple chat using Django REST Framework

## How to run

```shell
git clone https://github.com/Nexxel05/Django-REST-Simple-chat.git
cd Django-REST-Simple-chat
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
Create .env file in root directory and store there your 
SECRET_KEY like shown in .env_sample

```
python manage.py migrate
python manage.py runserver
```

Database is pre-populated with fixture data

## Credentials
* Username: admin
* password: 1qazcde3