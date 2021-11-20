from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Customer

def customer_profile(sender, instance, created, *args, **kwargs):
    if created:
        #obtenemos group
        group = Group.objects.get(name='customer')
        #the user is gonna be the instance
        #le añadimos el grupo a user
        instance.groups.add(group)
        #se crea un customer para el nuevo user
        Customer.objects.create(
            user=instance,
            name=instance.username,
            )
        print('Profile Created!')
#esta al pendiente en User cuando se crea algo
post_save.connect(customer_profile, User)