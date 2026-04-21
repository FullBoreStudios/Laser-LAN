from django.http import HttpResponse


def home(request):
    return HttpResponse("Laser LAN base app is online.")
