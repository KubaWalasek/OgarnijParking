import pytest
from django.contrib.auth.models import User
from accounts.models import User



@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='Testpassword'
    )

@pytest.fixture
def userprofile(user):
    return User.objects.create(
        user=user,
        first_name='testname',
        last_name='testlastname',
        post_code='12345',
        city='testcity',
        street='teststreet',
        street_number='123',
        door_number='456',
        phone_number='1234567890'
    )
