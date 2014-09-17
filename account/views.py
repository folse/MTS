#coding=utf-8
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django import forms
from models import User_Profile

from forms import RegisterForm, PasswordForm
import re

@never_cache
def login(request, template_name='account/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm):
    """Displays the login form and handles the login action."""

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or ' ' in redirect_to:
                redirect_to = '/website'
            
            # Heavier security check -- redirects to http://example.com should 
            # not be allowed, but things like /view/?param=http://example.com 
            # should be allowed. This regex checks if there is a '//' *before* a
            # question mark.
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                    redirect_to = '/website/list'
            
            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)
    
    request.session.set_test_cookie()
    
    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to
    }, context_instance=RequestContext(request))

def register(request):
    if request.method == 'GET':
        return render_to_response('account/register.html', {'regForm':RegisterForm()},
            context_instance=RequestContext(request), content_type="application/xhtml+xml")
    else:
        regForm = RegisterForm(request.POST)
        if regForm.is_valid():
            data = regForm.cleaned_data
            
            #Parse Signup
            userObjectId = parse_signup(data)

            user = User.objects.create_user(data['username'].lower(), data['email'], data['password'])
            user.email, user.is_staff, user.is_active, user.is_superuser = data['email'], True, True, False
            user_profile = User_Profile(user=user)
            user_profile.objectId, user_profile.description, user_profile.userType = userObjectId, '', 1 
            user_profile.save()
            user.save()
            from django.contrib.auth import authenticate, login
            #login() saves the user's ID in the session
            user = authenticate(username=data['username'], password=data['password'])
            login(request, user) 
            return HttpResponseRedirect('/website')
        else:
            return render_to_response('account/register.html', {'regForm':regForm},
                context_instance=RequestContext(request), content_type="application/xhtml+xml")
   
def parse_signup(data):
    from parse_rest.user import User
    u = User.signup(data['username'], data['password'], email=data['email'])
    return u.objectId

@user_passes_test(lambda u: u.is_authenticated(), login_url='/account/login')
def profile(request):
    if request.method == "GET":
        return HttpResponseRedirect('/website/list')
    
@user_passes_test(lambda u: u.is_authenticated(), login_url='/account/login')
def settings(request):
    if request.method == "GET":
        return render_to_response('account/settings.html',
         {'PasswordForm':PasswordForm()},
        context_instance=RequestContext(request), content_type="application/xhtml+xml")
    else:
        form = PasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('account/password_change_success.html')
        else:
            return render_to_response('account/settings.html',
                 {'PasswordForm':PasswordForm()},
                context_instance=RequestContext(request), content_type="application/xhtml+xml")
				
def password_reset(request):
    if request.method == 'GET':
		return render_to_response('account/password_reset.html', {'regForm':RegisterForm()},
		context_instance=RequestContext(request), content_type="application/xhtml+xml")
    else:
        regForm = RegisterForm(request.POST)
        if regForm.is_valid():
            data = regForm.cleaned_data
            user = User.objects.create_user(data['username'], data['email'], data['password'])
            user.email, user.is_staff, user.is_active, user.is_superuser = data['email'], True, True, False
            user.save()
            from django.contrib.auth import authenticate, login
            #login() saves the user's ID in the session
            user = authenticate(username=data['username'], password=data['password'])
            login(request, user)           
            return HttpResponseRedirect('/website/list')
        else:
            return render_to_response('account/register.html', {'regForm':regForm},
                context_instance=RequestContext(request), content_type="application/xhtml+xml")

