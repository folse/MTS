from django.contrib import admin
from management import models
from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint

class Photo(Object):
	pass

class Category_Place(Object):
	pass

class Place(Object):
	register('MQRrReTdb9c82PETy0BfUoL0ck6xGpwaZqelPWX5','44mp6LNgEmYEfZMYZQz16ncu7oqcnncGFtz762nC')
	print 'parse register'

class PlaceAdmin(admin.ModelAdmin):

	def save_model(self, request, obj, form, change):
		photo = Photo()
		photo.url = obj.photo
		photo.save()


		category = Category_Place.Query.filter(name=obj.category)[0]
		if category:
			pass
		else:
			category = Category_Place()
			category.name = obj.category
			category.save()


		place = Place()
		place.name = obj.name
		place.phone = obj.phone
		place.news = obj.news
		place.open_hour = obj.open_hour
		place.description = obj.description
		place.location = GeoPoint(latitude = obj.latitude, longitude = obj.longitude)
		place.save()

		photoIdList = [photo.objectId]
		place.addRelation('photos', 'Photo', photoIdList)

		categoryIdList = [category.objectId]
		place.addRelation('category', 'Category_Place', categoryIdList)
		
		

admin.site.register(models.Place,PlaceAdmin)
