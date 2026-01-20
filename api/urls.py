from django.urls import path

from .views import classify_ads_api


urlpatterns = [
    path("ads_classifier/", classify_ads_api, name="classify_ads_api")
]
