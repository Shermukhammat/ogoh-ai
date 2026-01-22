from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from dashboard.models import TelegramChat
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import login as dlogin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import serializers
from django.db.models import Count
from django.views.decorators.http import require_GET
from . import TokenAuthentication, REST_API_TOKEN


class TelegramChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramChat
        fields = ['id', 'tg_id', 'username', 'title', 'created_at',
                  'last_checked_at', 'type', 'risk']



class TelegramChatViewSet(viewsets.ModelViewSet):
    queryset = TelegramChat.objects.all()
    serializer_class = TelegramChatSerializer
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'
    lookup_value_regex = r'\d+'

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, id=None):
        return super().retrieve(request, id)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, id=None):
        return super().update(request, id)

    def destroy(self, request, id=None):
        return super().destroy(request, id)


@require_GET
def get_new_chat(request: HttpRequest) -> JsonResponse:
    token = request.GET.get('token')
    if token != REST_API_TOKEN:
        return JsonResponse({'ok': False, 'error': 'Invalid token'}, status=401)
    
    chats = TelegramChat.objects.filter(risky = 'risky', ).order_by('created_at')[:1]
    return JsonResponse({
        'ok': True,})


@require_GET
def get_chat(request: HttpRequest):
    token = request.GET.get('token')
    if token != REST_API_TOKEN:
        return JsonResponse({'ok': False, 'error': 'Invalid token'}, status=401)
    
    tg_id = request.GET.get('tg_id')
    if not tg_id:
        return JsonResponse({'ok': False, 'error': 'tg_id parameter is required'}, status=400)
    
    chat = TelegramChat.objects.filter(tg_id=tg_id).first()
    if not chat:
        return JsonResponse({'ok': False, 'error': 'Chat not found'}, status=404)
    
    serializer = TelegramChatSerializer(chat)
    return JsonResponse(serializer.data)