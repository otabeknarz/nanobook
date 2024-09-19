from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        return render(request, "main.html")

    return render(request, "index.html")


def logout_page(request):
    logout(request)
    return redirect("core:index")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("core:index")
        else:
            return render(request, "page2.html", {"error": "Parol yoki login xato"})
    return render(request, "page2.html")
