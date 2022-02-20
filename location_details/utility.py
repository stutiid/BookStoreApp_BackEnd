from django.http import QueryDict


class RequestUpdater:
    """
    To update the request object according to the modal class
    """

    @staticmethod
    def get_lat_long(request):
        """
        To separate the latitude and longitude from the geolocation provided by the user. And then updating the request
        object with the obtained latitude and longitude
        :param request: request object containing details of new location to be added
        :return: updated request object else exception will be raised
        """
        try:
            geolocation = request.data['geolocation']
            if "," not in geolocation:
                raise ValueError("use comma to separate lat and long in geolocation field")
            coordinates = geolocation.split(",")
            if isinstance(request.data, QueryDict):
                request.data._mutable = True
            request.data.update({'latitude': float(coordinates[0])})
            request.data.update({'longitude': float(coordinates[1])})
            return request
        except Exception as exp:
            raise exp
