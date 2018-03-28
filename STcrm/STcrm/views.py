from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout

import json

# Create your views here.

def acc_login(request):
    if request.method == 'GET':
        return render(request, 'acc_login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = authenticate(request,username=username,password=password)
        if user_obj:
            login(request,user_obj)
            return redirect(request.GET.get('next', '/'))
            # return redirect('/sale/')
        else:
            error_msg = 'Wrong username or password!'
            return render(request, 'acc_login.html', {'error_msg':error_msg})


def acc_logout(request):
    logout(request)
    return redirect('/login/')

