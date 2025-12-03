from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from .models import *
from django.core.mail import send_mail
                                          
                                          
@receiver(post_save, sender =Participant )
def after_saving_participant(sender, instance, **kwargs):
        send_mail(
            subject='From Lndmark.Tj',
            message=f'User {instance.user.email}  was added  to bus {instance.bus.name}',
            from_email=instance.user.email,
            recipient_list=['haitova.farangis10@gmail.com', 'hafizovm001@gmail.com']
        )
        
        send_mail(
            subject='From Lndmark.Tj',
            message=f'Welcome  {instance.user.email}, you were sucessifully added to tournament with bus {instance.bus.name}',
            from_email=instance.user.email,
            recipient_list=[instance.user.email]
        )
        print('sent1')

                                      
@receiver(pre_delete, sender = Participant )
def before_deleting_participant(sender, instance, **kwargs):
        send_mail(
            subject='From Lndmark.Tj',
            message=f'User {instance.user.email} is going to remove itself from {instance.bus.name}',
            from_email=instance.user.email,
            recipient_list=['haitova.farangis10@gmail.com', 'hafizovm001@gmail.com']
        )
        
        send_mail(
            subject='From Lndmark.Tj',
            message=f'Dear  {instance.user.email}, you were sucessifully reoved from  tournament with bus {instance.bus.name}',
            from_email=instance.user.email,
            recipient_list=[instance.user.email]
        )
        print('sent2')
   
    
