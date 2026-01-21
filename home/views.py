import json

from django.http import HttpRequest
from django.shortcuts import render

from api.views.classifier import classify

# Create your views here.

LABELS = {
    "drug_ad": "Giyohvandlik reklama",
    "drug_related": "Giyohvandlik haqida gap",
    "benign": "Xavfsiz kontent",
    "uncertain": "Noaniq holat",
}


def home_view(request: HttpRequest):
    context = {
        "input_text": "",
        "result": None,
        "result_pretty": "",
        "label_display": "",
        "error": "",
    }
    if request.method == "POST":
        text = request.POST.get("message", "").strip()
        context["input_text"] = text
        if not text:
            context["error"] = "Iltimos, tasniflash uchun matn kiriting."
        else:
            try:
                result = classify(text)
                context["result"] = result
                context["label_display"] = LABELS.get(
                    result.get("label"), "Noma'lum"
                )
                context["result_pretty"] = json.dumps(
                    result, indent=2, ensure_ascii=False
                )
            except Exception as exc:
                context["error"] = f"Tasniflashda xatolik: {exc}"
    return render(request, "home.html", context)
