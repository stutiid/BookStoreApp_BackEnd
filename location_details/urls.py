from django.urls import path
from location_details import views

urlpatterns = [
    path(r'location/', views.LocationView.as_view(), name="location"),
    path(r'name_suggestions/', views.SuggestionsView.as_view(), name="suggestions")
]
