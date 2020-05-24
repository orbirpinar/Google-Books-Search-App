from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


#user kaydedildiğinde bir sinyal gönder receiver sinyali alıyor
#user oluşturulursa profili oluştur demek ifli kod  
@receiver(post_save, sender=User)
def create_profile(sender,instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


#instance olan userın prfilini kaydediyor eğer böyle yapmasaydık her seferinde profil resmi için modelı migrate etmemiz gerekirdi.
@receiver(post_save, sender=User)
def saved_profile(sender,instance, **kwargs):
	instance.profile.save()
