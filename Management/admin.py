from django.contrib import admin
from Management import models
from django.http import HttpResponseRedirect
import urllib


def export_selected_objects(modeladmin, request, queryset):
	return HttpResponseRedirect("/path/")

class Place(models.Place):
	def save_related(self, request, obj, form, change):
		return HttpResponseRedirect("/path/")

admin.site.register(models.Place)

admin.site.add_action(export_selected_objects)