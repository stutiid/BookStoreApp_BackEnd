from rest_framework import serializers
from location_details.models import LocationDetails


class LocationSerializer(serializers.ModelSerializer):
    """
    LocationSerializer is used to format complex request object to simple python objects
    """

    class Meta:
        model = LocationDetails
        fields = ['id', 'name', 'latitude', 'longitude', 'description', 'state', 'population']

    def create(self, validated_data):
        """
        To add a new location with the given details and then save the location on the database.
        :param validated_data: contains the location details as dictionary with which new location is to be created
        :return: the new location object
        """
        location = LocationDetails(
            name=validated_data['name'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
            description=validated_data['description'],
            state=validated_data['state'],
            population=validated_data['population']
        )
        location.save()
        return location
