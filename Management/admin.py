from django.contrib import admin
from Management import models
import urllib


class PlaceAdmin(admin.ModelAdmin):

	def save_model(self, request, obj, form, change):
		urllib.urlopen('http://baidu.com').read()


admin.site.register(models.Place,PlaceAdmin)
