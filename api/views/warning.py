import json
from dashboard.models import WarningMessage, TelegramChat
from django.http import JsonResponse, HttpRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from . import REST_API_TOKEN


@csrf_exempt
@require_POST
def create_warning_message(request: HttpRequest) -> JsonResponse:
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse(
            {"ok": False, "error": "Invalid JSON body"},
            status=400
        )

    if data.get("token") != REST_API_TOKEN:
        return JsonResponse(
            {"ok": False, "error": "Invalid token"},
            status=401
        )

    chat_id = data.get("chat_id")
    message_id = data.get("message_id")
    content = data.get("content")
    user_id = data.get("user_id")
    
    if not chat_id or not message_id or not content:
        return JsonResponse(
            {"ok": False, "error": "chat_id, message_id and content are required"},
            status=400
        )
    
    tg_chat = TelegramChat.objects.filter(tg_id=chat_id).first()
    if not tg_chat:
        return JsonResponse(
            {"ok": False, "error": "Chat not found"},
            status=404
        )

    WarningMessage.objects.create(
        chat=tg_chat,
        message_id=message_id,
        content=content,
    )

    return JsonResponse({"ok": True})
