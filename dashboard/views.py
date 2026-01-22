from django.http import HttpRequest
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import TelegramChat, WarningMessage


@staff_member_required
def dashboard_view(request: HttpRequest):
    chats_qs = TelegramChat.objects.all().order_by("-created_at")
    warnings_qs = WarningMessage.objects.select_related("chat").order_by("-created_at")

    chats_page_number = request.GET.get("chats_page", 1)
    warnings_page_number = request.GET.get("warnings_page", 1)

    chats_page_obj = Paginator(chats_qs, 8).get_page(chats_page_number)
    warnings_page_obj = Paginator(warnings_qs, 7).get_page(warnings_page_number)

    context = {
        "chats_page_obj": chats_page_obj,
        "warnings_page_obj": warnings_page_obj,
        "chats_total": chats_qs.count(),
        "warnings_total": warnings_qs.count(),
        "risky_total": chats_qs.filter(risk="risky").count(),
        "listening_total": chats_qs.filter(listening=True).count(),
    }
    return render(request, "dashboard.html", context)
