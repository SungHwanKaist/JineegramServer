# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout, authenticate

from .forms import LoginForm, SignupForm
from .serializers import UserSerializer

def login(request):
    if request.method == 'POST':
        next = request.GET.get('next')

        login_form = LoginForm(request=request, data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            django_login(request, user)
            return redirect(next if next else 'post:post_list')
        login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = LoginForm()

    context = {
        'login_form': login_form,
    }
    return render(request, 'member/login.html', context)


def logout(request):
    django_logout(request)
    return redirect('post:post_list')

def signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            django_login(request, user)
            return redirect('post:post_list')
    else:
        signup_form = SignupForm()

    context = {
        'signup_form': signup_form,
    }
    return render(request, 'member/signup.html', context)