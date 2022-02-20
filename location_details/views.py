import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.views import APIView
from location_details.models import LocationDetails
from location_details.serializers import LocationSerializer
from location_details.utility import RequestUpdater

logger = logging.getLogger('exceptions')
logger.setLevel(logging.DEBUG)
log_handlers = {
    "file_debug": logging.FileHandler("exceptions.log".format(name=__name__, level="DEBUG"), mode="w"),
}
logger.addHandler(log_handlers['file_debug'])


class LocationView(APIView):
    """
    View handles the adding of new location and fetching of available location details by location name
    """

    def get(self, request):
        """
        To get a particular location details whose name is given by user. If particular name does not match with any
        then exception will be raised.
        :param request:- request object containing location name on the basis of which location list will be filtered
        :return:- list containing location details object else if some exception occur then appropriate response will be
                  returned
        """
        try:
            name = request.GET.get('name')
            if name is None:
                raise ValueError("enter name to get the details for")
            location = LocationDetails.objects.filter(name=name.title())
            if not location:
                raise ObjectDoesNotExist("entered name not found")
            serializer = LocationSerializer(location, many=True)
            return JsonResponse({"message": "Location details", "data": serializer.data})
        except ValueError as exception:
            logger.exception(exception.__traceback__)
            return JsonResponse({"message": f"{exception.__str__()}"},
                                status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as exception:
            logger.exception(exception.__traceback__)
            return JsonResponse({"message": f"{exception.__str__()}"},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as exception:
            logger.exception(exception.__traceback__)
            return JsonResponse({"message": f"generic error : {exception.__str__()}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """
        New Location details will be added through this method, first the details will be validated and then the new
        location will be saved on to the database
        :param request: have the data in json format with details for the new location details to be added
        :return: new location details else if some exception occur then appropriate response will be returned
        """
        try:
            request = RequestUpdater.get_lat_long(request)
            serializer = LocationSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return JsonResponse({"message": "location is added successfully", "data": serializer.data})
        except ValidationError as exception:
            logger.exception(exception.__traceback__)
            return JsonResponse({"message": f"validation error : {exception.__str__()}"},
                                status=status.HTTP_400_BAD_REQUEST)
        except APIException as exception:
            logger.exception(exception.__traceback__)
            return JsonResponse({"message": f"api error : {exception.__str__()}"},
                                status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as exception:
            logger.exception(exception.__traceback__)
            return JsonResponse({"message": f"generic error : {exception.__str__()}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SuggestionsView(APIView):
    """
    View fetching of available location details which matched the filter provided by user
    """

    def get(self, request):
        """
        To provide suggestions to user of the location names already present in database by matching the location name's
        initials with the one provided by user.
        :param request: request object containing first letter of possibble location name on the basis of which suggestions
                        is to be provided
        :return: list containing location details object else if some exception occur then appropriate response will be
                 returned
        """
        try:
            suggestion = request.GET.get("initial")
            if suggestion is None:
                raise ValueError("enter initial to get the suggestions")
            location = LocationDetails.objects.filter(name__contains=suggestion.title())
            serializer = LocationSerializer(location, many=True)
            return JsonResponse({"message": "Location details", "data": serializer.data})
        except ValueError as exception:
            logger.exception(exception.__traceback__)
            return JsonResponse({"message": f"value error: {exception.__str__()}"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception:
            logger.exception(exception.__traceback__)
            return JsonResponse({"message": f"generic error : {exception.__str__()}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
