import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.conftest import user
from django.contrib.auth.models import User
from django.urls import reverse
from accounts.models import CustomUser

#################################   REGISTER VIEW TESTS ################################################################
@pytest.mark.django_db
def test_register_view(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()


@pytest.mark.django_db
def test_register_view_post_success(client):
    url = reverse('register')
    data = {'username': 'testuser',
            'password_1': 'Testpassword',
            'password_2': 'Testpassword',
            'email': 'testuser@example.com'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert User.objects.filter(username='testuser').exists()
    assert UserProfile.objects.filter(user__username='testuser').exists()

@pytest.mark.django_db
def test_register_view_post_fail_username(client):
    url = reverse('register')
    user = User.objects.create_user(username='testuser', email='emial@email.com', password='Testpassword')
    data = {'username': 'testuser',
            'password_1': 'Testpassword',
            'password_2': 'Testpassword',
            'email': 'email@email.com'
    }
    response = client.post(url, data)
    print(response.content.decode())
    assert response.status_code == 200
    assert "A user with that username already exists" in response.content.decode()

@pytest.mark.django_db
def test_register_view_post_fail_email(client):
    url = reverse('register')
    user = User.objects.create_user(username='testuser', email='email@email.com', password='testpassword')
    data = {'username': 'testuser1',
            'password_1': 'testpassword',
            'password_2': 'testpassword',
            'email': 'email@email.com'
    }
    response = client.post(url, data)
    print(response.content.decode())
    assert response.status_code == 200
    assert 'Użytkownik z tym adresem e-mail już istnieje' in response.content.decode()


#################################   LOGIN VIEW TESTS ################################################################


@pytest.mark.django_db
def test_loginView_get(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()

@pytest.mark.django_db
def test_login_view_post_success(client, user):
    url = reverse('login')
    data ={'username': 'testuser',
           'password': 'Testpassword'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('user_account')


@pytest.mark.django_db
def test_login_view_post_fail(client, user):
    url = reverse('login')
    data ={'username': 'testuser',
           'password': 'testpasswordd'}
    response = client.post(url, data)
    assert 'Invalid username or password' in response.content.decode()

@pytest.mark.django_db
def test_logout_view(client, user):
    client.force_login(user)
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('login')

######################################  User Account View Tests ##################################################

@pytest.mark.django_db
def test_user_account_view(client, user):
    client.force_login(user)
    url = reverse('user_account')
    response = client.get(url)
    assert response.status_code == 200
    assert '<form' in response.content.decode()

@pytest.mark.django_db
def test_user_account_view_get_no_profile_data(client, user):
    client.force_login(user)
    url = reverse('user_account')
    # przed wejściem na widok profil nie istnieje
    assert not UserProfile.objects.filter(user=user).exists()
    response = client.get(url)
    assert response.status_code == 200
    assert 'testuser' in response.content.decode()
    assert 'testuser@example.com' in response.content.decode()
    # po GET profil został utworzony, ale bez danych (NULL)
    assert UserProfile.objects.filter(user=user).exists()
    profile = UserProfile.objects.get(user=user)
    assert profile.first_name is None
    assert profile.last_name is None
    assert profile.city is None



@pytest.mark.django_db
def test_user_account_view_get_with_profile_data(client, user, userprofile):
    client.force_login(user)
    url = reverse('user_account')
    response = client.get(url)
    print(response.content.decode())
    assert response.status_code == 200
    assert 'testuser' in response.content.decode()
    assert 'testlastname' in response.content.decode()
    assert 'testname' in response.content.decode()
    assert '12345' in response.content.decode()
    assert 'testcity' in response.content.decode()
    assert 'teststreet' in response.content.decode()
    assert '123' in response.content.decode()
    assert '456' in response.content.decode()
    assert '1234567890' in response.content.decode()

@pytest.mark.django_db
def test_user_account_view_post_success_user_data_new_email(client, user):
    client.force_login(user)
    url = reverse('user_account')
    data = {'username': 'testuser',
            'password': 'testpassword',
            'email': 'newemail@test.com'
            }
    response = client.post(url, data, follow=True)
    print(response.content.decode())
    assert response.status_code == 200
    assert 'newemail@test.com' in response.content.decode()
    assert 'Account updated successfully!' in response.content.decode()

@pytest.mark.django_db
def test_user_account_view_post_success_no_data_updated(client, user):
    client.force_login(user)
    url = reverse('user_account')
    data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password_1': 'Testpassword',
        'password_2': 'Testpassword',
        }
    response = client.post(url, data)

    print(response.content.decode())
    assert 'No data updated' in response.content.decode()


@pytest.mark.django_db
def test_user_account_view_post_success_profile_data_updated(client, user, userprofile):
    client.force_login(user)
    url = reverse('user_account')
    data ={
            'username': 'testuser',
            'email': 'test@example.com',
            'password_1': 'Testpassword',
            'password_2': 'Testpassword',
            'first_name': 'Jan',
            'last_name': 'Jankowski',
            'city': 'warszawa',
    }
    response = client.post(url, data, follow=True)
    print(response.content.decode())
    assert response.status_code == 200
    assert 'Jan' in response.content.decode()
    assert 'Jankowski' in response.content.decode()
    assert 'warszawa' in response.content.decode()
    assert 'Account updated successfully!' in response.content.decode()



class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)























