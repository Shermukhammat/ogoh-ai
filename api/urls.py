from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import classify_ads_api, TelegramChatViewSet, get_new_chat, check_message, get_chat, create_warning_message


router = DefaultRouter(trailing_slash=False)
router.register(r'tg_chats', TelegramChatViewSet)

urlpatterns = [
    path("ads_classifier/", classify_ads_api, name="classify_ads_api"),
    path("new_chat", get_new_chat, name="get_new_chat"),
    path("check_message", check_message, name="check_message"),
    path("tg_chat", get_chat, name="get_chat"),
    path("create_warning", create_warning_message, name="create_warning_message"),

    path('', include(router.urls)),
]
