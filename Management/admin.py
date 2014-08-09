from django.contrib import admin
from Management import models
from parse_rest.connection import register
from parse_rest.datatypes import Object, Pointer, Relation,GeoPoint

class Photo(Object):
	pass

class Category(Object):
	pass

class Place(Object):
	register('MQRrReTdb9c82PETy0BfUoL0ck6xGpwaZqelPWX5','44mp6LNgEmYEfZMYZQz16ncu7oqcnncGFtz762nC')
	print 'parse register'

class PlaceAdmin(admin.ModelAdmin):

	def save_model(self, request, obj, form, change):
		photo = Photo()
		photo.url = obj.photo
		photo.save()
		print photo.objectId

		category = Category()
		category.name = obj.category
		category.save()

		place = Place()
		place.name = obj.name
		place.phone = obj.phone
		place.news = obj.news
		place.open_hour = obj.open_hour
		place.description = obj.description
		#place.addRelation('photos', 'Place', photo.objectId)
		place.category = Pointer(category)
		place.location = GeoPoint(latitude = obj.latitude, longitude = obj.longitude)
		place.save()

admin.site.register(models.Place,PlaceAdmin)
