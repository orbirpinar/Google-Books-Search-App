from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse

from PIL import Image

class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg',upload_to='profile_pics')
	bio = models.TextField(max_length=30,blank=True)
	birth_date = models.DateField(null=True,blank=True)
	location = models.CharField(max_length=30,null=True,blank=True)

	def get_absolute_url(self):
		return reverse('home',args=[str(self.pk)])




	def __str__(self):
		return f"{self.user.username} Profili"


	def save(self,*args,**kwargs):
		#run to save method parent class
		super().save(*args,**kwargs)
		img = Image.open(self.image.path)

		#eğer profile pic genişliği  veya boyu 300 den büyükse onları 300 yap
		if img.height>300 or img.width>300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)