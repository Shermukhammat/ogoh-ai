import json

from django.http import HttpRequest
from django.shortcuts import render

from .classifier import classify

def dashboard_view(request: HttpRequest):
    context = {
        "input_text": "",
        "result": None,
        "result_pretty": "",
        "error": "",
    }
    if request.method == "POST":
        text = request.POST.get("message", "").strip()
        context["input_text"] = text
        if not text:
            context["error"] = "Please enter text to classify."
        else:
            try:
                result = classify(text)
                context["result"] = result
                context["result_pretty"] = json.dumps(
                    result, indent=2, ensure_ascii=False
                )
            except Exception as exc:
                context["error"] = f"Classification failed: {exc}"
    return render(request, "dashboard.html", context)
