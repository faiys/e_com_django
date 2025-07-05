from django.shortcuts import render,redirect
from django.http import HttpResponse

## is authenticated go to store page else go to login page
def unauthenticated_users(view_func):
	def wrapper_func(request,*args,**kwargs):
		if request.user.is_authenticated:
			return redirect('viewstores')
		else:
			return view_func(request,*args,**kwargs)
	return wrapper_func

## Allowed user permission using django groups ['admin','customer']
def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request,*args,**kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			if group in allowed_roles:
				return view_func(request,*args,**kwargs)
			else:
				return HttpResponse("You are not authorized to view page")
		return wrapper_func
	return decorator

## Auto redirect seperate admin and customers page using groups
# def admin(view_func):
# 	def wrapper_func(request,*args,**kwargs):

# 		group = None
# 		if request.user.groups.exists():
# 			group = request.user.groups.all()[0].name

# 		if group == 'customer':
# 			return redirect('viewstores')

# 		if group == 'admin':
# 			return view_func(request,*args,**kwargs)
# 	return wrapper_func