from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_librarian:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Identifiant ou mot de passe invalide")
    return render(request, 'librarian/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')


def dashboard(request):
    return render(request, 'librarian/dashboard.html')