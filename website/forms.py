#coding=utf-8

from django import forms
	
class Add_Place_Form(forms.Form):
	name = forms.CharField(max_length=32, label='Name', required=True, help_text='*')
	category = forms.CharField(max_length=32, label='Category', required=True, help_text='*')
	phone = forms.CharField(max_length=32, label='Phone', required=False, help_text='')
	photo = forms.CharField(max_length=512, label='Photo', required=False, help_text='')
	open_hour = forms.CharField(max_length=128, label='Open Hour', required=False, help_text='max 128 characters')
	latitude = forms.CharField(label='Latitude', required=False, help_text='')
	longitude = forms.CharField(label='Longitude', required=False, help_text='')
	news = forms.CharField(max_length=512, label='News', required=False, widget=forms.Textarea, help_text='max 512 characters')
	description = forms.CharField(max_length=512, label='Description', required=False, widget=forms.Textarea, help_text='max 512 characters')
