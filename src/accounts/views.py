from django.shortcuts import render, redirect
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout
)

# Import forms (forms.py)
from .forms import UserLoginForm, UserRegisterForm

# Create your views here.
"""
	VIEWS:
		- login_view --> get(username, password), action(login), login.html
		- register_view --> get(username, email, password, password_check), action(register), signup.html
		- logout_view --> action(logout), null
"""
def login_view(request):
	next = request.GET.get('next')
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		login(request, user)
		if next:
			return redirect(next)
		return redirect('/')
	context = {
		'form': form,
	}
	return render(request, "login.html", context)

def register_view(request):
	next = request.GET.get('next')
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()
		new_user = authenticate(username=user.username, password=password)
		login(request, new_user)
		if next:
			return redirect(next)
		return redirect('/')
	context = {
		'form': form,
	}
	return render(request, "signup.html", context)

def logout_view(request):
	logout(request)
	return redirect('/')