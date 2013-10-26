import django.contrib.auth.views as views
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login

import pong_app.forms

def register(request):
    if request.method == 'POST':
        form = pong_app.forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            login(request, new_user)
            return HttpResponseRedirect("/")
    else:
        form = pong_app.forms.CustomUserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })


def password_reset(request):
    response = views.password_reset(
        request,
        template_name='registration/password_reset.html',
        email_template_name='registration/password_reset_email.html',
        post_reset_redirect='/accounts/password_reset_done/'
    )
    return response


def password_reset_done(request):
    return views.password_reset_done(request, 'registration/password_reset_done.html')


def password_reset_confirm(request, uidb36=None, token=None):
    extra_context = { 
        'uidb36': uidb36,
        'token': token
    }

    return views.password_reset_confirm(
        request,
        uidb36=uidb36,
        token=token,
        template_name='registration/password_reset_confirm.html',
        post_reset_redirect='/accountsgl/password_reset_complete/',
        extra_context=extra_context
    )


def password_reset_complete(request):
    return views.password_reset_complete(
        request,
        template_name='registration/password_reset_complete.html'
    )