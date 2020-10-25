# django_chat
A simple one to one text chat app where you can send a friend request using the person username.

## installation
After clonning the repo, execute the following commands in the exact following order

```bash
source venv/bin/activate
```

```bash
python get-pip.py pip=19.3
```

```bash
pip install -r requirements.txt
```

```bash
sudo apt update
sudo apt upgrade
```

```bash
sudo install redis-server
sudo install memcached
```

## Starting the application
To start the application run the following commands in order

```bash
sudo service redis-server start
sudo service memcached start
```

```bash
cd src
python manage.py runserver
```

## Technologies used in the project
This project uses the following technologies:

- django
- djangorestframework
- channels
- redis
- memcached
- vue js
