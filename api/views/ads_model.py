import json
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .classifier import classify
from . import REST_API_TOKEN

def _extract_message(request: HttpRequest) -> str:
    if request.content_type == "application/json":
        try:
            payload = json.loads(request.body or "{}")
        except json.JSONDecodeError:
            return ""
        return str(payload.get("message", "")).strip()
    return request.POST.get("message", "").strip()


@csrf_exempt
@require_POST
def classify_ads_api(request: HttpRequest) -> JsonResponse:
    text = _extract_message(request)
    if not text:
        return JsonResponse(
            {"ok": False, "error": "Please provide message in the request body."},
            status=400,
        )
    try:
        result = classify(text)
    except Exception as exc:
        return JsonResponse(
            {"ok": False, "error": f"Classification failed: {exc}"},
            status=500,
        )
    return JsonResponse({"ok": True, "input_text": text, "result": result})



@require_GET
def check_message(request: HttpRequest) -> JsonResponse:
    if request.GET.get("token") != REST_API_TOKEN:
        return JsonResponse({"ok": False, "error": "Invalid token"}, status=401)
    
    text = request.GET.get("message", "").strip()
    if not text:
        return JsonResponse(
            {"ok": False, "error": "Please provide message in the 'message' query parameter."},
            status=400,
        )
    
    try:
        result = classify(text)
    except Exception as exc:
        return JsonResponse(
            {"ok": False, "error": f"Classification failed: {exc}"},
            status=500,
        )
    return JsonResponse({"ok": True, "text": text, "result": result})