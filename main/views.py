from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse
from joinpartner.models import Partner

def show_main(request):
    context = {
        'apps' : 'Rentara+',
    }

    return render(request, "main.html", context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if not request.POST.get('remember_me'):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(1209600)
            
            return JsonResponse({
                'status': True,
                'username': user.username,
                'is_staff': user.is_staff, 
                'message': 'Successfully Logged In!'
            })
        else:
            return JsonResponse({
                'status': False,
                'message': 'Invalid credentials.'
            }, status=401)

    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:show_main'))
    response.delete_cookie('user_logged_in')
    return response
