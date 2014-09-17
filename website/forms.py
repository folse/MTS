#coding=utf-8

from django import forms

from parse_rest.connection import register
from parse_rest.datatypes import Object
from parse_rest.user import User

class Category_Place(Object):
	register('MQRrReTdb9c82PETy0BfUoL0ck6xGpwaZqelPWX5','44mp6LNgEmYEfZMYZQz16ncu7oqcnncGFtz762nC')
	print 'parse register'
	
class Place_Form(forms.Form):
	
	PLACE_CATEGORY_CHOICES = [(category.objectId, category.name) for category in Category_Place.Query.all()]
	name = forms.CharField(max_length=32, label='Name', required=True, help_text='*')
	address = forms.CharField(max_length=256, label='Address', required=True, help_text='*')
	category = forms.ChoiceField(label='Category', required=True, choices=PLACE_CATEGORY_CHOICES, help_text='*')
	phone = forms.CharField(max_length=32, label='Phone', required=False, help_text='')
	#photo = forms.CharField(max_length=512, label='Photo', required=False, help_text='Please use comma to split the photo links')
	#open_hour = forms.CharField(max_length=128, label='Open Hour', required=False, help_text='max 128 characters')
	#latitude = forms.CharField(label='Latitude', required=False, help_text='')
	#longitude = forms.CharField(label='Longitude', required=False, help_text='')
	tags = forms.CharField(max_length=256, label='Tags', required=False, help_text='separate multiple keywords with commas')
	has_park = forms.BooleanField(label='Parking Place Available', required=False, help_text='')
	has_alcohol = forms.BooleanField(label='Serve Alcohol Drinks', required=False, help_text='')
	phone_reservation = forms.BooleanField(label='Phone Reservation', required=False, help_text='')
	delivery = forms.BooleanField(label='Support Delivery', required=False, help_text='')
	news = forms.CharField(max_length=512, label='News', required=False, widget=forms.Textarea, help_text='max 512 characters')
	description = forms.CharField(max_length=512, label='Description', required=False, widget=forms.Textarea, help_text='max 512 characters')
