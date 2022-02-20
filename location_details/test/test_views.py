import json

import pytest
from mixer.backend.django import mixer
from rest_framework.reverse import reverse

# pytestmark=pytest.mark.django_db
from location_details.models import LocationDetails


@pytest.mark.django_db
class TestLocationView:

    def test_adding_new_location_details(self, client):
        url = reverse("location")
        data = {
            "name": "Bangalore",
            "geolocation": "12.9699,77.5980",
            "description": "Bengaluru (also called Bangalore) is the capital of India's southern Karnataka state. " +
                           "The center of India's high-tech industry, the city is also known for its parks and " +
                           "nightlife.",
            "state": "Karnataka",
            "population": 13707000
        }
        response = client.post(url, data)
        print(response.content)
        assert response.status_code == 200 and b'location is added successfully' in response.content

    def test_adding_new_location_with_invalid_details(self, client):
        url = reverse("location")
        data = {
            "name": "Bangalore",
            "geolocation": "129699,77.5980",
            "description": "Bengaluru (also called Bangalore) is the capital of India's southern Karnataka state. " +
                           "The center of India's high-tech industry, the city is also known for its parks and " +
                           "nightlife.",
            "state": "Karnataka",
            "population": 13707000
        }
        response = client.post(url, data)
        print(response.content)
        assert response.status_code == 400 and b'validation error' in response.content

    def test_adding_new_location_with_missing_details(self, client):
        url = reverse("location")
        data = {
            "name": "Bangalore",
            "geolocation": "129699,77.5980",
            "description": "Bengaluru (also called Bangalore) is the capital of India's southern Karnataka state. " +
                           "The center of India's high-tech industry, the city is also known for its parks and " +
                           "nightlife.",
            "population": 13707000
        }
        response = client.post(url, data)
        print(response.content)
        assert response.status_code == 400 and b'validation error' in response.content

    def test_adding_new_location_with_improper_geolocation(self, client):
        url = reverse("location")
        data = {
            "name": "Bangalore",
            "geolocation": "12.9699 77.5980",
            "description": "Bengaluru (also called Bangalore) is the capital of India's southern Karnataka state. " +
                           "The center of India's high-tech industry, the city is also known for its parks and " +
                           "nightlife.",
            "state": "Karnataka",
            "population": 13707000
        }
        response = client.post(url, data)
        print(response.content)
        assert response.status_code == 500
        assert b'generic error : use comma to separate lat and long in geolocation field' in response.content

    def test_get_location_details_by_name(self, client):
        url = reverse("location")
        location = mixer.blend(LocationDetails, name="Pune", population=7764000)
        location.save()
        location = mixer.blend(LocationDetails, name="Panaji", population=40017)
        location.save()
        url = url + "?name=Pune"
        response = client.get(url)
        assert response.status_code == 200
        response = json.loads(response.content)
        assert 'Pune' == response['data'][0]["name"]

    def test_get_location_details_for_name_not_existing(self, client):
        url = reverse("location")
        url = url + "?name=Delhi"
        response = client.get(url)
        assert response.status_code == 404
        assert b'entered name not found' in response.content

    def test_get_location_details_by_not_providing_name(self, client):
        url = reverse("location")
        location = mixer.blend(LocationDetails, name="Mumbai", population=23355000)
        location.save()
        response = client.get(url)
        assert response.status_code == 400
        assert b'enter name to get the details for' in response.content

    def test_get_location_details_by_name_case_insensitive(self, client):
        url = reverse("location")
        location = mixer.blend(LocationDetails, name="Panaji", population=40017)
        location.save()
        url = url + "?name=panaji"
        response = client.get(url)
        assert response.status_code == 200
        response = json.loads(response.content)
        assert 'Panaji' == response['data'][0]["name"]

    def test_get_suggestions_by_location_name_initials(self, client):
        url = reverse("suggestions")
        location = mixer.blend(LocationDetails, name="Mumbai", population=23355000)
        location.save()
        url = url + "?initial=m"
        response = client.get(url)
        assert response.status_code == 200
        response = json.loads(response.content)
        assert 'Mumbai' == response['data'][0]["name"]

    def test_get_suggestions_by_not_providing_name_initials(self, client):
        url = reverse("suggestions")
        location = mixer.blend(LocationDetails, name="Ahmedabad", population=7410000)
        location.save()
        response = client.get(url)
        print(response.content)
        assert response.status_code == 400 and b'enter initial to get the suggestions' in response.content
