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
from django.views.generic.list import ListView
from django.views.generic import DetailView

from forms import Add_Place_Form
from models import PlaceModel

from parse_rest.user import User
from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint

class Photo(Object):
	pass

class Category_Place(Object):
	pass

class Relation(Object):
    pass

class Place(Object):
	#register('MQRrReTdb9c82PETy0BfUoL0ck6xGpwaZqelPWX5','44mp6LNgEmYEfZMYZQz16ncu7oqcnncGFtz762nC')
	#print 'parse register'
    pass

class PlaceListView(ListView):
    template_name = 'website/place/place_list.html'
    def get_queryset(self):
        places = Place.Query.filter(user=User.Query.get(objectId=self.request.user.user_profile.objectId)).limit(2)
        return places
        
@user_passes_test(lambda u: u.is_authenticated(), login_url='/account/login')
def place_edit(request, objectId):
    if request.method == "GET":
        place = Place.Query.get(objectId=objectId)
        placeForm = Add_Place_Form({'name':place.name,'address':place.address,'phone':place.phone,'open_hour':place.open_hour,'latitude':place.location.latitude,'longitude':place.location.longitude,'news':place.news,'description':place.description})
        print placeForm
        return render_to_response('website/place/place_edit.html', {'Add_Place_Form':placeForm},
        context_instance=RequestContext(request), content_type="application/xhtml+xml")
        
# class PlaceDetailView(DetailView):
#     model = PlaceModel
#     fields = ['name']
#     template_name_suffix = '_edit'
#     def get_queryset(self,pk):
#         pass
#         # template_name = 'website/place/place_edit.html'
#         # def get_queryset(self):
#         #     place = Place.Query.get(objectId='0FzG70BYlH')
#         #     return place

@user_passes_test(lambda u: u.is_authenticated(), login_url='/account/login')
def place_add(request):
    if request.method == "GET":
        return render_to_response('website/place/place_add.html', {'Add_Place_Form':Add_Place_Form()},
        context_instance=RequestContext(request), content_type="application/xhtml+xml")
    else:
    	data = request.POST
        form = Add_Place_Form(data)
        place = Place()
        place.name = data.get('name')
        place.news = data.get('news')
        place.phone = data.get('phone')
        place.address = data.get('address')
        place.open_hour = data.get('open_hour')
        place.description = data.get('description')
        place.location = GeoPoint(latitude = float(data.get('latitude')), longitude = float(data.get('longitude')))
        place.save()

        # photo = Photo()
        # photo.url = data.get('photo')
        # photo.save()
        # photoIdList = [photo.objectId]
        # place.addRelation('photos', 'Photo', photoIdList)

        user = User.Query.get(objectId=request.user.user_profile.objectId)
        if user:
            place.addRelation('user', '_User', [user.objectId])

        category = Category_Place.Query.get(objectId=data.get('category'))
        if category:
        	place.addRelation('category', 'Category_Place', [data.get('category')])
        else:
            pass
        	# category = Category_Place()
        	# category.name = data.get('category')
        	# category.save()
        	# place.addRelation('category', 'Category_Place', [category.objectId])
        return HttpResponseRedirect('/website/success')

