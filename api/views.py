#coding=utf-8
from django.http import HttpResponse
from django.contrib.auth.models import User

import sys
import json
import urllib2

from parse_rest.user import User
from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint

from qiniu import Auth
from qiniu import put_data

reload(sys)
sys.setdefaultencoding('utf-8')

class Photo(Object):
	pass

class Category_Place(Object):
	pass

class Relation(Object):
    pass

class Place(Object):
	pass
	# register('MQRrReTdb9c82PETy0BfUoL0ck6xGpwaZqelPWX5','44mp6LNgEmYEfZMYZQz16ncu7oqcnncGFtz762nC')
	# print 'parse register'

def upload_to_qiniu(request):
	if request.method == 'POST':
		data = request.POST
		qiniu = Auth('StbRobqxbTkicUShT5AlRXqXs6I7LCEZCk-tmLXz', 'RuWkSQA1pXyjI_Rn_W4aRylC6cj0q_sgT3m7Xc39')
		token = qiniu.upload_token('ts-image1')
		file_url = data.get('file_url')
		file_name = data.get('file_name')
		#conn = urllib2.urlopen(file_url)  
		#data = conn.read()
		try:
			request = urllib2.Request(file_url)
			request.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')  
			opener = urllib2.build_opener()
			data = opener.open(request).read()
			ret, info = put_data(token, file_name, data)
			result = info.text_body
			result_json = json.loads(result)
			result_file_name = result_json['key']
			jsonData = {'respcd':'0000','file_name':result_file_name}
		except Exception, e:
			print e
			jsonData = {'respcd':'0002','msg':'upload image error'}
	else:
		jsonData = {'respcd':'0001','msg':'only support POST'}
	return HttpResponse(json.dumps(jsonData), content_type="application/json")

def login(request):
	if request.method == 'POST':
		data = request.POST
		from django.contrib.auth import authenticate
		user = authenticate(username=data.get('username'), password=data.get('password'))
		from django.contrib.auth import login
		login(request,user)
		sessionid = request.session.session_key
		jsonData = {'respcd':'0000','sessionid':sessionid,'api':'login'}
	else:
		jsonData = {'respcd':'0001','msg':'only support POST','api':'login'}
	return HttpResponse(json.dumps(jsonData), content_type="application/json")

def add_place(request):
	if request.method == 'POST':
		data = request.POST
		place = Place()
        place.name = data.get('name')
        place.news = data.get('news')
        place.phone = data.get('phone')
        place.types = data.get('types')
        place.address = data.get('address')
        place.open_hour = data.get('open_hour')
        place.description = data.get('description')
        place.google_photos = data.get('google_photos')
        place.location = GeoPoint(latitude = float(data.get('latitude')), longitude = float(data.get('longitude')))
        place.save()

        user = User.Query.get(objectId=request.user.user_profile.objectId)
        if user:
            place.addRelation('user', '_User', [user.objectId])

        category = Category_Place.Query.get(objectId=data.get('category'))
        if category:
        	place.addRelation('category', 'Category_Place', [data.get('category')])

		jsonData = {'respcd':'0000','api':'add_place'}
	else:
		jsonData = {'respcd':'0001','msg':'only support POST','api':'add_place'}
	return HttpResponse(json.dumps(jsonData), content_type="application/json")
