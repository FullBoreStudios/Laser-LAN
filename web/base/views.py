# import render
from django.shortcuts import render

def home(request):



    return render(request, 'base/index.html', {

    })
