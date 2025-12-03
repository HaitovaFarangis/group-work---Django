from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from .models import *
from django.core.mail import send_mail
                                          
                                          
@receiver(post_save, sender =Participant )
def after_saving_participant(sender, instance, **kwargs):
    try:
        send_mail(
            subject='From Lndmark.Tj',
            message=f'User {instance.user.email} added himself to bus {instance.bus.title}, {instance.bus.landmarks}',
            from_email=instance.user.from_email,
            recipient_list=['haitova.farangis10@gmail.com', 'hafizovm001@gmail.com']
        )
        
        send_mail(
            subject='From Lndmark.Tj',
            message=f'Welcome  {instance.user.email}, you were sucessifully added to tournamentwith bus {instance.bus.name}',
            from_email=instance.user.from_email,
            recipient_list=[instance.user.email]
        )
        print('sent')
        return{
        'send':True,
        'message':"Admin recieved that user added himself to bus."
        }
    except Exception as e:
        return{
        'send':False,
        'message':str(e)
        }
    
