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
from blog.models import Blog, Comment, Catagory
from faker import Faker
faker = Faker()
for _ in range(100):
    Blog.objects.create(name=faker.sentence(), text=faker.paragraph())

for blog in Blog.objects.all():
    comments = [Comment(text=faker.paragraph(), blog=blog) for _ in range(3)]
    Comment.objects.bulk_create(comments)

Catagory.objects.create(name="Python")
Catagory.objects.create(name="Java")
Catagory.objects.create(name="Scala")
Catagory.objects.create(name="Javascript")
Catagory.objects.create(name="Microscrvices")
Catagory.objects.create(name="Database")
