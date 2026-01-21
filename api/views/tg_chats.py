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
from . import TokenAuthentication




class TelegramChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramChat
        fields = ['tg_id', 'username', 'first_name', 'last_name', 'created_at']


class TelegramChatViewSet(viewsets.ModelViewSet):
    queryset = TelegramChat.objects.all()
    serializer_class = TelegramChatSerializer
    authentication_classes = [TokenAuthentication]
    lookup_field = 'tg_id'
    lookup_value_regex = r'\d+'

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, tg_id=None):
        return super().retrieve(request, tg_id)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, tg_id=None):
        return super().update(request, tg_id)

    def destroy(self, request, tg_id=None):
        return super().destroy(request, tg_id)