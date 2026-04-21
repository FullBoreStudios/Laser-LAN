from django.http import HttpResponse


def home(request):
    return HttpResponse("Laser LAN is online. API docs live at /api/docs.")
