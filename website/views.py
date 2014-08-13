#coding=utf-8
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect


from forms import Add_Place_Form
from decimal import Decimal
from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint

class Photo(Object):
	pass

class Category_Place(Object):
	pass

class Place(Object):
	register('MQRrReTdb9c82PETy0BfUoL0ck6xGpwaZqelPWX5','44mp6LNgEmYEfZMYZQz16ncu7oqcnncGFtz762nC')
	print 'parse register'
        
@user_passes_test(lambda u: u.is_authenticated(), login_url='/account/login')
def list(request):
    if request.method == "GET":
        return HttpResponseRedirect('/website/list')

@user_passes_test(lambda u: u.is_authenticated(), login_url='/account/login')
def add_place(request):
    if request.method == "GET":
        return render_to_response('website/place/place_add.html', {'Add_Place_Form':Add_Place_Form()},
        context_instance=RequestContext(request), content_type="application/xhtml+xml")
    else:
    	data = request.POST
        form = Add_Place_Form(data)
        place = Place()
        place.name = data.get('name')
        place.phone = data.get('phone')
        place.news = data.get('news')
        place.open_hour = data.get('open_hour')
        place.description = data.get('description')
        place.location = GeoPoint(latitude = float(data.get('latitude')), longitude = float(data.get('longitude')))
        place.save()

        # photo = Photo()
        # photo.url = data.get('photo')
        # photo.save()
        # photoIdList = [photo.objectId]
        # place.addRelation('photos', 'Photo', photoIdList)

        category = Category_Place.Query.filter(name=data.get('category'))
        if category:
        	place.addRelation('category', 'Category_Place', [category[0].objectId])
        else:
        	category = Category_Place()
        	category.name = data.get('category')
        	category.save()
        	place.addRelation('category', 'Category_Place', [category.objectId])
        return HttpResponseRedirect('/website/list')


