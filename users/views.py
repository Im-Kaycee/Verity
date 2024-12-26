from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy
# Create your views here.

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate user with the username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('voting')  # Redirect to a success page after login
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('user_login')  # Redirect back to the login page for retry
    else:
        return render(request, 'login.html')


def logout_user(request):
  logout(request)
  messages.success(request, ('Logout Successful'))
  return redirect('index')
