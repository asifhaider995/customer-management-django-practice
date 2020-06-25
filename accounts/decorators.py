from django.http import HttpResponse
from django.shortcuts import redirect

def anon_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if not request.user.is_anonymous:
			return redirect('../')
		else:	
			return view_func(request, *args, **kwargs)
	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
				# print(group)

			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse("You are not authorized")
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request,*args, **kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name
			print(group)
			if group == 'customers':
				return redirect('accounts:user')
			if group == 'admins':
				return view_func(request, *args, **kwargs)
	return wrapper_function