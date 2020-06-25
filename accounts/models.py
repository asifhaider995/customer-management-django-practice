import datetime

from django.db import models
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=10, null=False)
	last_name = models.CharField(max_length=10)
	profile_pic = models.ImageField(default="prof.png",null=True)
	phone = models.CharField(max_length=15)
	email = models.EmailField(null=False)
	date_created = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.first_name +" "+ self.last_name

	def get_name(self):
		return	self.first_name +" "+ self.last_name 

	def get_absolute_url(self):
		return reverse("accounts:customers", kwargs={"id": self.id})


class Tag(models.Model):
	"""docstring for Tag"""
	name = models.CharField(max_length=25, default='DefaultTag')

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORIES = (
		('SP', 'Sports'),
		('FA', 'Fashion'),
		('EN', 'Entertainment'),
		('CO', 'Consumables'),
		('EL', 'Electronics'),
		('HC', 'HealthCare'),
		('OT', 'Others')
	)
	name = models.CharField(max_length=255, null=False)
	description = models.CharField(max_length=500, blank=True,null=True)
	price = models.DecimalField(max_digits=4,decimal_places=2)
	category = models.CharField(max_length=2, choices=CATEGORIES, default='OT')
	stock = models.IntegerField(verbose_name='Remaining')
	featured = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)
	tag = models.ManyToManyField(Tag)


	def __str__(self):
		return self.name


class Order(models.Model):
	STATUS = (
		('DEL', 'Delivered'),
		('PEN', 'Pending'),
		('OFD', 'Out for Delivery')
	)
	reference = models.CharField(max_length=10,null=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=3, choices=STATUS, default='PEN')

	def __str__(self):
		return self.reference
