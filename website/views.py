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

class Tag(Object):
    pass

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
        places = Place.Query.filter(user=User.Query.get(objectId=self.request.user.user_profile.objectId)).limit(100)
        return places

@user_passes_test(lambda u: u.is_authenticated(), login_url='/account/login')
def place_upload(request):
    if request.method == "GET":
        return render_to_response('website/place/place_upload.html', {'Add_Place_Form':Add_Place_Form()},
        context_instance=RequestContext(request), content_type="application/xhtml+xml")

@user_passes_test(lambda u: u.is_authenticated(), login_url='/account/login')
def place_edit(request, objectId):
    place = Place.Query.get(objectId=objectId)
    if request.method == "GET":
        category = Category_Place.Query.relation_filter(category__relation=place)._relation_fetch()
        placeForm = Add_Place_Form(initial={'name':place.name,'address':place.address, 'category':category['objectId'], 'phone':place.phone,'open_hour':place.open_hour,'latitude':place.location.latitude,'longitude':place.location.longitude,'news':place.news,'description':place.description})
        return render_to_response('website/place/place_edit.html', {'Add_Place_Form':placeForm,'objectId':objectId,'categoryObjectId':category['objectId']},
        context_instance=RequestContext(request), content_type="application/xhtml+xml")
    else:
        data = request.POST
        #form = Add_Place_Form(data)
        place.name = data.get('name')
        place.news = data.get('news')
        place.phone = data.get('phone')
        place.address = data.get('address')
        place.open_hour = data.get('open_hour')
        place.description = data.get('description')
        place.has_park = data.get('has_park')
        place.has_alcohol = data.get('has_alcohol')
        place.phone_reservation = data.get('phone_reservation')
        place.location = GeoPoint(latitude = float(data.get('latitude')), longitude = float(data.get('longitude')))
        place.save()

        photo = Photo()
        photo.url = data.get('menu_photo')
        photo.save()
        photoIdList = [photo.objectId]
        place.addRelation('photos', 'Photo', photoIdList)

        place.removeRelation('category', 'Category_Place', [data.get('oldCategory')])
        place.addRelation('category', 'Category_Place', [data.get('category')])

        return HttpResponseRedirect('/website/success')
        
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

        mon_open_hour = 'Mon ' + data.get('mon_open_hour') + ':' + data.get('mon_open_minute') + '~' + data.get('mon_close_hour') + ':' + data.get('mon_close_minute')
        tue_open_hour = 'Tue ' + data.get('tue_open_hour') + ':' + data.get('tue_open_minute') + '~' + data.get('tue_close_hour') + ':' + data.get('tue_close_minute') + '/n'
        wed_open_hour = 'Web ' + data.get('wed_open_hour') + ':' + data.get('web_open_minute') + '~' + data.get('web_close_hour') + ':' + data.get('web_close_minute') + '/n'
        thur_open_hour = 'Thur ' + data.get('thur_open_hour') + ':' + data.get('thur_open_minute') + '~' + data.get('thur_close_hour') + ':' + data.get('thur_close_minute') + '/n'
        fri_open_hour = 'Fri ' + data.get('fri_open_hour') + ':' + data.get('fri_open_minute') + '~' + data.get('fri_close_hour') + ':' + data.get('fri_close_minute') + '/n'
        sta_open_hour = 'Sta ' + data.get('sta_open_hour') + ':' + data.get('sta_open_minute') + '~' + data.get('sta_close_hour') + ':' + data.get('sta_close_minute') + '/n'
        sun_open_hour = 'Sun ' + data.get('sun_open_hour') + ':' + data.get('sun_open_minute') + '~' + data.get('sun_close_hour') + ':' + data.get('sun_close_minute')
        open_hour = mon_open_hour + tue_open_hour + wed_open_hour + thur_open_hour + fri_open_hour + sta_open_hour + sun_open_hour

        place = Place()
        place.name = data.get('name')
        place.news = data.get('news')
        place.phone = data.get('phone')
        place.address = data.get('address')
        place.open_hour = data.get('open_hour')
        place.description = data.get('description')
        place.has_park = bool(data.get('has_park'))
        place.has_alcohol = bool(data.get('has_alcohol'))
        place.phone_reservation = bool(data.get('phone_reservation'))
        #place.location = GeoPoint(latitude = float(data.get('latitude')), longitude = float(data.get('longitude')))
        place.save()

        menuPhotoUrls = data.get('menu_photo').split(',')
        for photoUrl in menuPhotoUrls :
            photo = Photo()
            photo.url = photoUrl
            photo.menu_category = True
            photo.save()
            photoIdList.append(photo.objectId)

        productPhotoUrls = data.get('product_photo').split(',')
        for photoUrl in productPhotoUrls :
            photo = Photo()
            photo.url = photoUrl
            photo.product_category = True
            photo.save()
            photoIdList.append(photo.objectId)

        environmentPhotoUrls = data.get('environment_photo').split(',')
        for photoUrl in environmentPhotoUrls :
            photo = Photo()
            photo.url = photoUrl
            photo.environment_category = True
            photo.save()
            photoIdList.append(photo.objectId)

        otherPhotoUrls = data.get('other_photo').split(',')
        for photoUrl in otherPhotoUrls :
            photo = Photo()
            photo.url = photoUrl
            photo.other_category = True
            photo.save()
            photoIdList.append(photo.objectId)

        place.addRelation('photos', 'Photo', photoIdList)
        
        user = User.Query.get(objectId=request.user.user_profile.objectId)
        if user:
            place.addRelation('user', '_User', [user.objectId])

        category = Category_Place.Query.get(objectId=data.get('category'))
        if category:
        	place.addRelation('category', 'Category_Place', [data.get('category')])

        tagNames = data.get('tags').split(',')
        tagList = []
        for tagName in tagNames:
            existTags = Tag.Query.filter(name=tagName)
            if existTags.count() == 0:
                tag = Tag()
                tag.name = tagName
                tag.save()
                tagList.append(tag.objectId)
            else:
                tagList.append(existTags[0].objectId)

        if len(tagList) > 0:
            place.addRelation('tag', 'Tag', tagList)

        return HttpResponseRedirect('/website/success')

