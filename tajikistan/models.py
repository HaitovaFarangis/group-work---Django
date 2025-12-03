from django.db import models
from accounts.models import CustomUser

from django.db import models

class Landmark(models.Model):
    CATEGORY_CHOICES = (
        ('museum', 'Museum'),
        ('monument', 'Monument'),
        ('park', 'Park'),
        ('historical', 'Historical Site'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField()
    location = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    opening_hours = models.CharField(max_length=100, blank=True, null=True)
    entry_fee = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Bus(models.Model):
    name = models.CharField(max_length=100)  
    landmarks = models.ManyToManyField(Landmark, related_name='buses')  
    schedule = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ManyToManyField(CustomUser, related_name = 'user_bus', null=True, blank=True)

    def __str__(self):
        return self.name


class Participant(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='participants')
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='participants')
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email



    
    