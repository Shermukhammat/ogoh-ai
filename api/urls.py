from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import classify_ads_api, TelegramChatViewSet


router = DefaultRouter(trailing_slash=False)
router.register(r'tg_chats', TelegramChatViewSet)

urlpatterns = [
    path("ads_classifier/", classify_ads_api, name="classify_ads_api"),
    path('', include(router.urls)),
]
