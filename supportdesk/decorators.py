from django.http import HttpResponse
from django.shortcuts import redirect

def customers_only(view_func):
	"""This is a decorator that allows only customers access to the page 

	Args:
		view_func ([type]): view function
	"""    
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_staff:
			return redirect('request_list')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def agents_only(view_func):
	"""This is a decorator that allows only agents access to the page 

	Args:
		view_func ([type]): view function
	"""    
	def wrapper_func(request, *args, **kwargs):
		if not request.user.is_staff:
			return redirect('request_list')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func