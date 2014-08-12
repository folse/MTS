#coding=utf-8
import re
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django import forms

class RegisterForm(forms.Form):
	username = forms.CharField(max_length=30, label=_('名字'), required=True,
		help_text=_(' '))
	email = email = forms.EmailField(max_length=72, label=_('邮箱'), required=True,
			help_text=_(' '))
	password = forms.CharField(max_length=24, label=_('密码'), required=True, widget=forms.PasswordInput,
		help_text=_(' '))

	def clean_username(self):
		username = self.data.get('username')
		if len(username) < 3:
			raise forms.ValidationError(_('用户名最少3个字符'))
		m = re.search(u'[a-zA-Z0-9\u4e00-\u9fa5]+', username)
		if m and m.group(0) == username:
			if limit_name(username):
				raise forms.ValidationError(_('恭喜你，这个名字被和谐了'))
			try:
				User.objects.get(username=username)
			except ObjectDoesNotExist:
				return username
			else:
				raise forms.ValidationError(_('这个用户名已经被注册了'))
		else:
			raise forms.ValidationError(_('用户名中含有不合要求的字符'))
		
	def clean_password(self):
		password = self.data.get('password')
		if len(password) < 6:
			raise forms.ValidationError(_('密码最少6个字符'))
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
			raise forms.ValidationError(_('这个Email已经被注册了'))

class LoginForm(forms.Form):
	username = forms.CharField(max_length=28, label=_('邮箱'), required=True, help_text=_('Email'))
	password = forms.CharField(max_length=24, label=_('密码'), required=True, widget=forms.PasswordInput)

	def clean_username(self):
		try:
			username = self.data.get('username')
			m = re.search(u'[a-zA-Z0-9\.]+@[a-zA-Z0-9]+\.[a-zA-Z]+', username)
			if m and m.group(0):
				u = User.objects.get(email=m.group(0))
			else:
				u = User.objects.get(username=self.data.get('username'))
		except ObjectDoesNotExist:
			raise forms.ValidationError(_('该用户不存在'))
		return u.username

	def clean_password(self):
		try:
			from django.contrib.auth import authenticate
			user = authenticate(username=self.cleaned_data.get('username'), password=self.cleaned_data.get('password'))
			if not user:
				raise forms.ValidationError(_('用户名或密码错误'))
		except ObjectDoesNotExist:
			raise forms.ValidationError(_('用户名或密码错误'))
		return self.data.get('password')

def limit_name(name):
	LIIMIT_NAME = ['search', 'add', 'del', 'login', 'logout', 'apply', 'register', 'user', 'friend', 'group', 'company']
	if name in LIIMIT_NAME:
		return True
	return False

class PasswordForm(forms.Form):
	oldpassword = forms.CharField(max_length=24,label=_('当前密码'),required=True,widget=forms.PasswordInput)	
	newpassword = forms.CharField(max_length=24,label=_('新密码'),required=True,widget=forms.PasswordInput)
	newpwdcfm = forms.CharField(max_length=24,label=_('确认新密码'),required=True,widget=forms.PasswordInput)	
	def clean_newpassword(self):
		if self.data.get('newpassword') != self.data.get('newpwdcfm'):
			raise forms.ValidationError(_('新密码跟确认新密码不匹配'))
		return self.data.get('newpassword')
	
class PayAccountForm(forms.Form):
	realname = forms.CharField(max_length=32, label=_('真实姓名'), required=True, help_text=_('*'))
	identitycard = forms.CharField(max_length=32, label=_('身份证号'), required=True, help_text=_('*'))
	bank = forms.CharField(max_length=32, label=_('开户银行名称'), required=True, help_text=_('*'))
	payname = forms.CharField(max_length=32, label=_('银行帐号姓名'), required=True, help_text=_('*'))
	payaccount = forms.CharField(max_length=32, label=_('银行帐号'), required=True, help_text=_('*'))
	



