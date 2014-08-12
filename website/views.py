#coding=utf-8
from django.shortcuts import render
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
            
@user_passes_test(lambda u: u.is_authenticated(), login_url='/account/login')
def list(request):
    if request.method == "GET":
        return HttpResponseRedirect('/website/list')

