from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from .filters import OrderFilter
from .decorators import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
# from django.contrib.auth.forms import UserCreationForm
# Create your views here.

@anon_user
def login_view(request, *args, **kwargs):
	if request.method == 'POST':
		name = request.POST.get('username')
		pw = request.POST.get('password')
		user = authenticate(request, username=name, password=pw)
		# print(name)
		# print(pw)
		if user is not None:
			login(request, user)
			return redirect('../')
		else:
			messages.info(request, "Username and password don't match")
	context = {}
	return render(request, 'accounts/login.html', context)

def logout_view(request, *args, **kwargs):
	logout(request)
	return redirect('accounts:login')

@anon_user
def register_view(request, *args, **kwargs):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			# group = Group.objects.get(name='customers')
			# user.groups.add(group)

			
			# print(user)
			# print(username)
			# print(user.username)
			# print(group)
			# Customer.objects.create(
			# 	user = user
			# )
			messages.success(request, "Account created Successfully for " + form.cleaned_data.get('username'))
			return redirect('../')
		else:
			messages.error(request, 'Something went wront!')
	context = {
		'form':form
	}
	return render(request, 'accounts/register.html', context)

@login_required(login_url='accounts:login')
@admin_only
def home_view(request, *args, **kwargs):
	cus = Customer.objects.all()
	orders = Order.objects.all()
	total_customers = cus.count()
	total_orders = orders.count()
	delivered = orders.filter(status='DEL').count()
	pending = orders.filter(status='PEN').count()
	context = {
		'customers' : cus,
		'orders' : orders,
		't_o'  : total_orders,
		't_c'  : total_customers,
		'delivered' : delivered,
		'pen' : pending

	}
	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admins','customers'])
def product_view(request, *args, **kwargs):
	prod = Product.objects.order_by('-date_created')
	context = {
		'products' : prod
	}
	return render(request, 'accounts/products.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admins', 'staffUser'])
def customer_view(request, id, *args, **kwargs):
	cust = get_object_or_404(Customer,pk=id)
	# order = Order.objects.filter(customer=id)
	order = cust.order_set.all()
	o_c = order.count()

	myFilter = OrderFilter(request.GET, queryset=order)
	order = myFilter.qs

	context = {
		'customer' : cust,
		'orders'   : order,
		'o_c'	   : o_c,
		'myFilter' : myFilter
	}
	return render(request, 'accounts/customer.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admins','staffUser','customers'])
def create_order(request, id, *args, **kwargs):
	customer = Customer.objects.get(id=id)
	init_data = {
		'customer': customer
	}
	form = OrderForm(request.POST or None, initial=init_data)
	if form.is_valid():
		form.save()
		return redirect('home/')
	context = {
		'form' : form
	}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['admins',' staffUser','customers'])
def update_order(request, id, *args, **kwargs):
	obj = Order.objects.get(id=id)
	form = OrderForm(request.POST or None,instance=order)
	if form.is_valid():
			form.save()
			return redirect('/')
	context = {
		'form' : form
	}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customers'])
def user_view(request, *args, **kwargs):
	customer = request.user.customer
	orders = request.user.customer.order_set.all()
	total_orders = orders.count()
	delivered = orders.filter(status='DEL').count()
	pending = orders.filter(status='PEN').count()

	context = {
		'customers' : customer,
		'orders' : orders,
		't_o'  : total_orders,
		'delivered' : delivered,
		'pen' : pending


	}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='accounts:login')
@allowed_users(allowed_roles=['customers'])
def user_settings_view(request, *args, **kwargs):
	customer = request.user.customer
	form = CustomerForm(instance=customer)
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('accounts:user')
	context = {
		'form' : form
	}
	return render(request, 'accounts/user_settings.html', context)