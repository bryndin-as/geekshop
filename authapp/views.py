from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from authapp.models import User
from django.contrib import auth
from django.urls import reverse
from basket.models import Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required



def login (request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'authapp/login.html', context)



def register (request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегались!!!')
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = UserRegisterForm()
    context = {'form': form}

    return render(request, 'authapp/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        form = UserProfileForm(instance=request.user)

    baskets = Basket.objects.filter(user=request.user)
    context = {
        'form': form,
        'baskets': baskets,
        'total_guantity': sum(basket.guantity for basket in baskets),
        'total_sum': sum(basket.sum() for basket in baskets),
    }

    return render(request, 'authapp/profile.html', context)


