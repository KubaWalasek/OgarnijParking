import pytest
from django.urls import reverse
from parking_place.forms import AddUserToDistrictForm, DistrictSearchForm, PostCodeForm, StreetNameForm, \
CityNameForm, DistrictForm
from parking_place.conftest import district
from accounts.conftest import user



@pytest.mark.django_db
def test_district_view(client):
    url = reverse('district')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['district_search_form'], DistrictSearchForm)
    assert isinstance(response.context['add_user_to_district_form'], AddUserToDistrictForm)


@pytest.mark.django_db
def test_add_district_view(client):
    url = reverse('add_district')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['add_post_code_form'], PostCodeForm)
    assert isinstance(response.context['add_street_name_form'], StreetNameForm)
    assert isinstance(response.context['add_city_name_form'], CityNameForm)
    assert isinstance(response.context['create_district_form'], DistrictForm)


@pytest.mark.django_db
def test_add_user_to_district_view(client, user, district):
    client.force_login(user)
    data = {'selected_districts': [district.id]}
    url = reverse('add_user_to_district')
    response = client.post(url, data)
    assert response.status_code == 302
    assert district.signed_user.filter(id=user.id).exists()

@pytest.mark.django_db
def test_add_user_to_district_view_already_in_district(client, user, district):
    client.force_login(user)
    district.signed_user.add(user)
    data = {'selected_districts': [district.id]}
    url = reverse('add_user_to_district')
    response = client.post(url, data, follow=True)
    district.refresh_from_db()
    print (response.content.decode())
    assert response.status_code == 200
    assert 'You already joined' in response.content.decode()
    assert district.signed_user.filter(id=user.id).count() == 1







