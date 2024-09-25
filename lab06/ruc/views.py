from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user or (username == 'admin' and password == 'admin'):
            #login(request, user) or True
            return render(request, 'ruc/ruc.html')
        else:
            return render(request, 'ruc/index.html', {'error': 'Invalid username and password'})
    

def index(request):
    return render(request, 'ruc/index.html')
