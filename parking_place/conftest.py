import pytest

from parking_place.models import District, PostCode, CityName


@pytest.fixture
def postcode():
    postcode = PostCode.objects.create(
        post_code='12-345')
    return postcode

@pytest.fixture
def city_name():
    city_name = CityName.objects.create(
        city_name='test_city')
    return city_name


@pytest.fixture
def district(postcode, city_name):
    district = District.objects.create(
        district_name='test_district',
        city_name=city_name,
        post_code=postcode,
        street_name=None,
    )
    return district
