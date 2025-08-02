import os
import django
import random
from datetime import date, timedelta
from faker import Faker
from django.utils import translation

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  # <--- замени на своё!
django.setup()

from air_bnb_app.models import UserProfile, Property, Image, Booking, Review

fake = Faker()

def create_users():
    roles = ['guest', 'host']
    users = []
    for i in range(5):
        user = UserProfile.objects.create_user(
            username=fake.user_name(),
            email=fake.unique.email(),
            password='12345678',
            role=random.choice(roles),
            phone_number=fake.phone_number(),
            avatar='avatars/default.jpg'
        )
        users.append(user)
    return users



fake_en = Faker('en_US')
fake_ru = Faker('ru_RU')

def create_properties(hosts):
    props = []
    for _ in range(10):
        prop = Property.objects.create(
            owner=random.choice(hosts),
            title_en=fake_en.sentence(nb_words=4),
            description_en=fake_en.paragraph(),
            title_ru=fake_ru.sentence(nb_words=4),
            description_ru=fake_ru.paragraph(),
            price_per_night=round(random.uniform(1000, 10000), 2),
            city=fake_ru.city(),              # город на русском
            address=fake_ru.street_address(), # адрес на русском
            property_type=random.choice(['apartment', 'house', 'studio']),
            rules=random.choice(['no_smoking', 'pets_allowed']),
            max_guests=random.randint(1, 6),
            bedrooms=random.randint(1, 3),
            bathrooms=random.randint(1, 2),
            is_active=True
        )
        props.append(prop)
    return props


def create_images(properties):
    for prop in properties:
        for _ in range(random.randint(1, 3)):
            Image.objects.create(
                property=prop,
                image='property_images/sample.jpg'
            )

def create_bookings(properties, guests):
    bookings = []
    for _ in range(15):
        check_in = date.today() + timedelta(days=random.randint(1, 15))
        check_out = check_in + timedelta(days=random.randint(1, 5))
        booking = Booking.objects.create(
            property=random.choice(properties),
            guest=random.choice(guests),
            check_in=check_in,
            check_out=check_out,
            status=random.choice(['pending', 'approved', 'cancelled', 'rejected']),
        )
        bookings.append(booking)
    return bookings

def create_reviews(properties, guests):
    for _ in range(10):
        Review.objects.create(
            property=random.choice(properties),
            guest=random.choice(guests),
            rating=random.randint(1, 5),
            comment=fake.sentence(),
        )

def run():
    print("🧹 Очищаем старые данные...")
    Review.objects.all().delete()
    Booking.objects.all().delete()
    Image.objects.all().delete()
    Property.objects.all().delete()
    UserProfile.objects.exclude(is_superuser=True).delete()

    print("👥 Создаем пользователей...")
    users = create_users()
    hosts = [u for u in users if u.role == 'host']
    guests = [u for u in users if u.role == 'guest']

    print("🏠 Создаем жильё...")
    properties = create_properties(hosts)

    print("🖼️ Добавляем изображения...")
    create_images(properties)

    print("📅 Создаем бронирования...")
    create_bookings(properties, guests)

    print("📝 Создаем отзывы...")
    create_reviews(properties, guests)

    print("✅ Всё готово! База засеяна фейковыми данными 🎉")

if __name__ == '__main__':
    run()
