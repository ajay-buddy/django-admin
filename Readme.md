sudo docker-compose run web django-admin startproject djangoproject .
chown -R $USER:$USER .

python manage.py migrate
python manage.py migrate <app name>
python manage.py makemigrations
python manage.py makemigrations <app name>
python manage.py showmigrations
python manage.py createsuperuser

python manage.py shell

<!-- genereate fake data for Blog -->
from blog.models import Blog
from faker import Faker
for _ in range(100):
    Blog.objects.create(name=faker.sentence(), text=faker.paragraph())