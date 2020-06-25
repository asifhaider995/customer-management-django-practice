from .models import *
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def customer_profile(sender, instance, created, *args, **kwargs):
	if created:
		group = Group.objects.get(name='customers')
		instance.groups.add(group)


		Customer.objects.create(
			user=instance,
			first_name=instance.username,

		)
		print("Customer created")