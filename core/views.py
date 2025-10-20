from django.shortcuts import render


from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

User = get_user_model()

def validar_username(request):
    username = request.GET.get("usrname", "").strip()
    valid = True
    message = "Disponible ✅"

    if not username:
        valid = False
        message = "Ingresa un nombre de usuario"
    elif User.objects.filter(username__iexact=username).exists():
        valid = False
        message = "Este nombre ya está en uso"

    html = render_to_string("components/username_feedback.html", {
        "valid": valid,
        "message": message
    })

    return HttpResponse(html)