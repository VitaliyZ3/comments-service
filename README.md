# Comment service
## Service for displaying comments left by users

### Technology stack
 - django, drf
 - celery
 - redis
 - django-channels
 - Amazon RDS (MySQL)

# Quick start

### Start from docker-compose

Build application from docker-compose.yml file
```bash
docker-compose up --build
```
And open the <http://localhost:8000/swagger/> for view documentation

### Or start without docker-compose

#### Set up databases for comment application
Run redis docker instance
```bash
docker run -d --name redis-comments -p 6379:6379 redis
```
Create mysql database for application
```mysql
CREATE DATABASE database_1
```
and set your credentials for database connection in settings.py
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'database_1',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST':'localhost',
        'PORT':'3306',
    }
}
```
#### Set up django application

Create virtual environment
```bash
python3 -m venv venv
```
Enter venv
```bash
. ./venv/bin/activate #for Unix
. .\venv\Scripts\activate #for Windows
```
Install libs
```bash
pip install =r requirements.txt
```
Run celery worker and django application
```bash
celery -A comment_service  worker -l info -P gevent
python manage.py runserver
```
And now you`r project successfully started

# 