#coding=utf-8
import re
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django import forms

class RegisterForm(forms.Form):
	username = forms.CharField(max_length=30, label=_('Username'), required=True,
		help_text=_(' '))
	password = forms.CharField(max_length=24, label=_('Password'), required=True, widget=forms.PasswordInput,
		help_text=_(' '))
	email = email = forms.EmailField(max_length=72, label=_('Email'), required=True,
			help_text=_(' '))

	def clean_username(self):
		username = self.data.get('username')
		if len(username) < 3:
			raise forms.ValidationError(_('Username needs 3 characters at least'))
		m = re.search(u'[a-zA-Z0-9\u4e00-\u9fa5]+', username)
		if m and m.group(0) == username:
			if limit_name(username):
				raise forms.ValidationError(_('This username is not allowed'))
			try:
				User.objects.get(username=username)
			except ObjectDoesNotExist:
				return username
			else:
				raise forms.ValidationError(_('This username has been taken'))
		else:
			raise forms.ValidationError(_('This username includes invalid characters'))
		
	def clean_password(self):
		password = self.data.get('password')
		if len(password) < 6:
			raise forms.ValidationError(_('Password needs 6 characters at least'))
		try:
			User.objects.get(password=self.cleaned_data.get('password'))
		except ObjectDoesNotExist:
			return self.cleaned_data.get('password')
		
	def clean_email(self):
		try:
			User.objects.get(email=self.cleaned_data.get('email'))
		except ObjectDoesNotExist:
			return self.cleaned_data.get('email')
		else:
			raise forms.ValidationError(_('This email has been taken'))

class LoginForm(forms.Form):
	username = forms.CharField(max_length=28, label=_('Email'), required=True, help_text=_('Email'))
	password = forms.CharField(max_length=24, label=_('Password'), required=True, widget=forms.PasswordInput)

	def clean_username(self):
		try:
			username = self.data.get('username')
			m = re.search(u'[a-zA-Z0-9\.]+@[a-zA-Z0-9]+\.[a-zA-Z]+', username)
			if m and m.group(0):
				u = User.objects.get(email=m.group(0))
			else:
				u = User.objects.get(username=self.data.get('username'))
		except ObjectDoesNotExist:
			raise forms.ValidationError(_('This username does not exist'))
		return u.username

	def clean_password(self):
		try:
			from django.contrib.auth import authenticate
			user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
			if not user:
				raise forms.ValidationError(_('Username or password were incorrect'))
		except ObjectDoesNotExist:
			raise forms.ValidationError(_('Username or password were incorrect'))
		return self.data.get('password')

def limit_name(name):
	LIIMIT_NAME = ['search', 'add', 'del', 'login', 'logout', 'apply', 'register', 'user', 'friend', 'group', 'company']
	if name in LIIMIT_NAME:
		return True
	return False

class PasswordForm(forms.Form):
	oldpassword = forms.CharField(max_length=24,label=_('old password'),required=True,widget=forms.PasswordInput)	
	newpassword = forms.CharField(max_length=24,label=_('New password'),required=True,widget=forms.PasswordInput)
	newpwdcfm = forms.CharField(max_length=24,label=_('Confirm password'),required=True,widget=forms.PasswordInput)	
	def clean_newpassword(self):
		if self.data.get('newpassword') != self.data.get('newpwdcfm'):
			raise forms.ValidationError(_('Twice input is inconsistent'))
		return self.data.get('newpassword')
	



