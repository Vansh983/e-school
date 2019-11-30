from django import forms
from django.contrib.auth import (
	authenticate,
	get_user_model
)

"""
	FORMS:
		- UserLoginForm:
			FIELDS: username, password
			VIEW: login_view
		- UserRegisterForm:
			FIELDS: username, email, password, password_check
			VIEW: register_view
"""

User = get_user_model() # get standard user model
class UserLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args,**kwargs):
		super(UserLoginForm, self).__init__(*args,**kwargs)
		self.fields['username'].widget.attrs['placeholder'] = 'Username'
		self.fields['password'].widget.attrs['placeholder'] = 'Password'

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')

		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError('This user does not exist')
			if not user.check_password(password):
				raise forms.ValidationError('Incorrect password')
			if not user.is_active:
				raise forms.ValidationError('This user is not active')
		return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
	username = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput)
	password_check = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args,**kwargs)
		self.fields['username'].widget.attrs['placeholder'] = 'Username'
		self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
		self.fields['password'].widget.attrs['placeholder'] = 'Password'
		self.fields['password_check'].widget.attrs['placeholder'] = 'Confirm Password'

	class Meta:
		model = User
		fields = [
			'username',
			'email',
			'password',
			'password_check'
		]

	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get('email')
		email_qs = User.objects.filter(email=email)

		password = self.cleaned_data.get('password')
		password_check = self.cleaned_data.get('password_check')
		if email_qs.exists():
			raise forms.ValidationError('This email is already being used')
		if password != password_check:
			raise forms.ValidationError('Passwords do not match')
		return super(UserRegisterForm, self).clean(*args, **kwargs)