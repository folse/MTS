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

from forms import Place_Form

from parse_rest.user import User
from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint

import string
import hashlib
import os

class Tag(Object):
    pass

class Photo(Object):
	pass

class Category_Place(Object):
	pass

class Relation(Object):
    pass

class Place(Object):
    # register('MQRrReTdb9c82PETy0BfUoL0ck6xGpwaZqelPWX5','44mp6LNgEmYEfZMYZQz16ncu7oqcnncGFtz762nC')
    # print 'parse register'
    pass

class PlaceListView(ListView):
    template_name = 'website/place/place_list.html'
    def get_queryset(self):
        places = Place.Query.all().filter(user=User.Query.get(objectId=self.request.user.user_profile.objectId)).limit(100).order_by("-updatedAt")
        return places

@user_passes_test(lambda u: u.is_authenticated(), login_url='/account/login')
def place_success(request):
    if request.method == "GET":
        return render_to_response('website/place/place_success.html', {},
        context_instance=RequestContext(request), content_type="application/xhtml+xml")

@user_passes_test(lambda u: u.is_authenticated(), login_url='/account/login')
def place_edit(request, objectId):
    place = Place.Query.get(objectId=objectId)
    tagList = Tag.Query.relation_filter(tag__relation=place)._relation_fetch()
    tagString = ''
    for i in range(0, len(tagList)):
        tagString += tagList[i]['name']
        if i != len(tagList)-1:
            tagString += ','
    if request.method == "GET":
        category = Category_Place.Query.relation_filter(category__relation=place)._relation_fetch()[0]

        placeForm = Place_Form(initial={'name':place.name,'address':place.address, 'category':category['objectId'], 'phone':place.phone,'open_hour':place.open_hour,'news':place.news,'description':place.description,'has_park':place.has_park,'has_alcohol':place.has_alcohol,'phone_reservation':place.phone_reservation,'tags':tagString})

        mon_open_hour = ''
        mon_open_minute = ''
        mon_close_hour = ''
        mon_close_minute = ''

        tue_open_hour = ''
        tue_open_minute = ''
        tue_close_hour = ''
        tue_close_minute = ''

        wed_open_hour = ''
        wed_open_minute = ''
        wed_close_hour = ''
        wed_close_minute = ''

        thur_open_hour = ''
        thur_open_minute = ''
        thur_close_hour = ''
        thur_close_minute = ''

        fri_open_hour = ''
        fri_open_minute = ''
        fri_close_hour = ''
        fri_close_minute = ''

        sta_open_hour = ''
        sta_open_minute = ''
        sta_close_hour = ''
        sta_close_minute = ''

        sun_open_hour = ''
        sun_open_minute = ''
        sun_close_hour = ''
        sun_close_minute = ''

        openHourList = place.open_hour.split('\n')
        for i in range(0, len(openHourList)):
            openHourString = openHourList[i].split(' ')[1]
            if i == 0:
                mon_open_hour = openHourString.split('~')[0].split(':')[0]
                mon_open_minute = getMinuteLevel(openHourString.split('~')[0].split(':')[1])
                mon_close_hour = openHourString.split('~')[1].split(':')[0]
                mon_close_minute = getMinuteLevel(openHourString.split('~')[1].split(':')[1])
            elif i == 1:
                tue_open_hour = openHourString.split('~')[0].split(':')[0]
                tue_open_minute = getMinuteLevel(openHourString.split('~')[0].split(':')[1])
                tue_close_hour = openHourString.split('~')[1].split(':')[0]
                tue_close_minute = getMinuteLevel(openHourString.split('~')[1].split(':')[1])
            elif i == 2:
                wed_open_hour = openHourString.split('~')[0].split(':')[0]
                wed_open_minute = getMinuteLevel(openHourString.split('~')[0].split(':')[1])
                wed_close_hour = openHourString.split('~')[1].split(':')[0]
                wed_close_minute = getMinuteLevel(openHourString.split('~')[1].split(':')[1])
            elif i == 3:
                thur_open_hour = openHourString.split('~')[0].split(':')[0]
                thur_open_minute = getMinuteLevel(openHourString.split('~')[0].split(':')[1])
                thur_close_hour = openHourString.split('~')[1].split(':')[0]
                thur_close_minute = getMinuteLevel(openHourString.split('~')[1].split(':')[1])
            elif i == 4:
                fri_open_hour = openHourString.split('~')[0].split(':')[0]
                fri_open_minute = getMinuteLevel(openHourString.split('~')[0].split(':')[1])
                fri_close_hour = openHourString.split('~')[1].split(':')[0]
                fri_close_minute = getMinuteLevel(openHourString.split('~')[1].split(':')[1])
            elif i == 5:
                sta_open_hour = openHourString.split('~')[0].split(':')[0]
                sta_open_minute = getMinuteLevel(openHourString.split('~')[0].split(':')[1])
                sta_close_hour = openHourString.split('~')[1].split(':')[0]
                sta_close_minute = getMinuteLevel(openHourString.split('~')[1].split(':')[1])
            elif i == 6:
                sun_open_hour = openHourString.split('~')[0].split(':')[0]
                sun_open_minute = getMinuteLevel(openHourString.split('~')[0].split(':')[1])
                sun_close_hour = openHourString.split('~')[1].split(':')[0]
                sun_close_minute = getMinuteLevel(openHourString.split('~')[1].split(':')[1])

        return render_to_response('website/place/place_edit.html', {'Place_Form':placeForm,'objectId':objectId,'categoryObjectId':category['objectId'],
            'mon_open_hour':mon_open_hour,'mon_open_minute':mon_open_minute,'mon_close_hour':mon_close_hour,'mon_close_minute':mon_close_minute,
            'tue_open_hour':tue_open_hour,'tue_open_minute':tue_open_minute,'tue_close_hour':tue_close_hour,'tue_close_minute':tue_close_minute,
            'wed_open_hour':wed_open_hour,'wed_open_minute':wed_open_minute,'wed_close_hour':wed_close_hour,'wed_close_minute':wed_close_minute,
            'thur_open_hour':thur_open_hour,'thur_open_minute':thur_open_minute,'thur_close_hour':thur_close_hour,'thur_close_minute':thur_close_minute,
            'fri_open_hour':fri_open_hour,'fri_open_minute':fri_open_minute,'fri_close_hour':fri_close_hour,'fri_close_minute':fri_close_minute,
            'sta_open_hour':sta_open_hour,'sta_open_minute':sta_open_minute,'sta_close_hour':sta_close_hour,'sta_close_minute':sta_close_minute,
            'sun_open_hour':sun_open_hour,'sun_open_minute':sun_open_minute,'sun_close_hour':sun_close_hour,'sun_close_minute':sun_close_minute},
        context_instance=RequestContext(request), content_type="application/xhtml+xml")
    else:
        data = request.POST
        #form = Add_Place_Form(data)
        mon_open_hour = 'Mon ' + data.get('mon_open_hour') + ':' + data.get('mon_open_minute') + '~' + data.get('mon_close_hour') + ':' + data.get('mon_close_minute') + '\n'
        tue_open_hour = 'Tue ' + data.get('tue_open_hour') + ':' + data.get('tue_open_minute') + '~' + data.get('tue_close_hour') + ':' + data.get('tue_close_minute') + '\n'
        wed_open_hour = 'Wed ' + data.get('wed_open_hour') + ':' + data.get('wed_open_minute') + '~' + data.get('wed_close_hour') + ':' + data.get('wed_close_minute') + '\n'
        thur_open_hour = 'Thur ' + data.get('thur_open_hour') + ':' + data.get('thur_open_minute') + '~' + data.get('thur_close_hour') + ':' + data.get('thur_close_minute') + '\n'
        fri_open_hour = 'Fri ' + data.get('fri_open_hour') + ':' + data.get('fri_open_minute') + '~' + data.get('fri_close_hour') + ':' + data.get('fri_close_minute') + '\n'
        sta_open_hour = 'Sta ' + data.get('sta_open_hour') + ':' + data.get('sta_open_minute') + '~' + data.get('sta_close_hour') + ':' + data.get('sta_close_minute') + '\n'
        sun_open_hour = 'Sun ' + data.get('sun_open_hour') + ':' + data.get('sun_open_minute') + '~' + data.get('sun_close_hour') + ':' + data.get('sun_close_minute')
        open_hour = mon_open_hour + tue_open_hour + wed_open_hour + thur_open_hour + fri_open_hour + sta_open_hour + sun_open_hour

        place.name = data.get('name')
        place.news = data.get('news')
        place.phone = data.get('phone')
        place.address = data.get('address')
        place.open_hour = open_hour
        place.description = data.get('description')
        place.has_park = bool(data.get('has_park'))
        place.has_alcohol = bool(data.get('has_alcohol'))
        place.phone_reservation = bool(data.get('phone_reservation'))
        place.takeaway = bool(data.get('take_away'))
        #place.location = GeoPoint(latitude = float(data.get('latitude')), longitude = float(data.get('longitude')))
        place.save()

        photoIdList = []
        menuPhotoUrls = data.get('menu_photo').split(',')
        for photoUrl in menuPhotoUrls :
            if photoUrl != '0':
                photo = Photo()
                photo.url = photoUrl
                photo.menu_category = True
                photo.save()
                photoIdList.append(photo.objectId)

        productPhotoUrls = data.get('product_photo').split(',')
        for photoUrl in productPhotoUrls :
            if photoUrl != '0':
                photo = Photo()
                photo.url = photoUrl
                photo.product_category = True
                photo.save()
                photoIdList.append(photo.objectId)

        environmentPhotoUrls = data.get('environment_photo').split(',')
        for photoUrl in environmentPhotoUrls :
            if photoUrl != '0':
                photo = Photo()
                photo.url = photoUrl
                photo.environment_category = True
                photo.save()
                photoIdList.append(photo.objectId)

        otherPhotoUrls = data.get('other_photo').split(',')
        for photoUrl in otherPhotoUrls :
            if photoUrl != '0':
                photo = Photo()
                photo.url = photoUrl
                photo.other_category = True
                photo.save()
                photoIdList.append(photo.objectId)

        place.addRelation('photos', 'Photo', photoIdList)

        if data.get('oldCategory') != data.get('category'):
            print 'change category'
            place.removeRelation('category', 'Category_Place', [data.get('oldCategory')])
            place.addRelation('category', 'Category_Place', [data.get('category')])

        if  (hashlib.md5(tagString).hexdigest().upper() != hashlib.md5(data.get('tags')).hexdigest().upper()):
            print 'change tag'
            oldTagIdList = []
            for i in range(0, len(tagList)):
                oldTagIdList.append(tagList[i]['objectId'])
            place.removeRelation('tag', 'Tag', oldTagIdList)

            tagNames = data.get('tags').split(',')
            tagList = []
            for tagName in tagNames:
                existTags = Tag.Query.filter(name=tagName)
                if existTags.count() == 0:
                    tag = Tag()
                    tag.name = tagName.lower()
                    tag.save()
                    tagList.append(tag.objectId)
                else:
                    tagList.append(existTags[0].objectId)

            if len(tagList) > 0:
                place.addRelation('tag', 'Tag', tagList)

        return HttpResponseRedirect('/website/success')

def getMinuteLevel(minute):
    if minute == '15':
        return 1
    elif minute == '30':
        return 2
    elif minute == '45':
        return 3
    return 0
        
# class PlaceDetailView(DetailView):
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
        return render_to_response('website/place/place_add.html', {'Place_Form':Place_Form()},
        context_instance=RequestContext(request), content_type="application/xhtml+xml")
    else:
    	data = request.POST

        mon_open_hour = 'Mon ' + data.get('mon_open_hour') + ':' + data.get('mon_open_minute') + '~' + data.get('mon_close_hour') + ':' + data.get('mon_close_minute') + '\n'
        tue_open_hour = 'Tue ' + data.get('tue_open_hour') + ':' + data.get('tue_open_minute') + '~' + data.get('tue_close_hour') + ':' + data.get('tue_close_minute') + '\n'
        wed_open_hour = 'Wed ' + data.get('wed_open_hour') + ':' + data.get('wed_open_minute') + '~' + data.get('wed_close_hour') + ':' + data.get('wed_close_minute') + '\n'
        thur_open_hour = 'Thur ' + data.get('thur_open_hour') + ':' + data.get('thur_open_minute') + '~' + data.get('thur_close_hour') + ':' + data.get('thur_close_minute') + '\n'
        fri_open_hour = 'Fri ' + data.get('fri_open_hour') + ':' + data.get('fri_open_minute') + '~' + data.get('fri_close_hour') + ':' + data.get('fri_close_minute') + '\n'
        sta_open_hour = 'Sta ' + data.get('sta_open_hour') + ':' + data.get('sta_open_minute') + '~' + data.get('sta_close_hour') + ':' + data.get('sta_close_minute') + '\n'
        sun_open_hour = 'Sun ' + data.get('sun_open_hour') + ':' + data.get('sun_open_minute') + '~' + data.get('sun_close_hour') + ':' + data.get('sun_close_minute')
        open_hour = mon_open_hour + tue_open_hour + wed_open_hour + thur_open_hour + fri_open_hour + sta_open_hour + sun_open_hour

        place = Place()
        place.name = data.get('name')
        place.news = data.get('news')
        place.phone = data.get('phone')
        place.address = data.get('address')
        place.open_hour = open_hour
        place.description = data.get('description')
        place.has_park = bool(data.get('has_park'))
        place.has_alcohol = bool(data.get('has_alcohol'))
        place.phone_reservation = bool(data.get('phone_reservation'))
        place.takeaway = bool(data.get('take_away'))
        #place.location = GeoPoint(latitude = float(data.get('latitude')), longitude = float(data.get('longitude')))
        place.save()

        photoIdList = []
        menuPhotoUrls = data.get('menu_photo').split(',')
        for photoUrl in menuPhotoUrls :
            if photoUrl != '0':
                photo = Photo()
                photo.url = photoUrl
                photo.menu_category = True
                photo.save()
                photoIdList.append(photo.objectId)

        productPhotoUrls = data.get('product_photo').split(',')
        for photoUrl in productPhotoUrls :
            if photoUrl != '0':
                photo = Photo()
                photo.url = photoUrl
                photo.product_category = True
                photo.save()
                photoIdList.append(photo.objectId)

        environmentPhotoUrls = data.get('environment_photo').split(',')
        for photoUrl in environmentPhotoUrls :
            if photoUrl != '0':
                photo = Photo()
                photo.url = photoUrl
                photo.environment_category = True
                photo.save()
                photoIdList.append(photo.objectId)

        otherPhotoUrls = data.get('other_photo').split(',')
        for photoUrl in otherPhotoUrls :
            if photoUrl != '0':
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
                tag.name = tagName.lower()
                tag.save()
                tagList.append(tag.objectId)
            else:
                tagList.append(existTags[0].objectId)

        if len(tagList) > 0:
            place.addRelation('tag', 'Tag', tagList)

        return HttpResponseRedirect('/website/success')

