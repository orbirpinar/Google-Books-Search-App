from django.db import models

from django.contrib.auth.models import User


READ_STATUS = (
    ('R','Read'),
    ('W','Want To Read'),
    ('C','Currently Reading')
)

class Books(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book_id = models.CharField(max_length=30,unique=True)
    title = models.CharField(null=True,blank=True,max_length=100)
    author = models.CharField(null=True,blank=True,max_length=100)
    description = models.TextField(null=True,blank=True)
    read_status = models.CharField(choices=READ_STATUS,max_length=2)
    page_count = models.CharField(max_length=6,null=True,blank=True)
    image_url = models.CharField(max_length=50,blank=True, null=True)
    average_rating = models.CharField(max_length=20,null=True,blank=True)
    date_created = models.DateField(auto_now=False,auto_now_add=True)
    date_updated = models.DateField(auto_now=True,auto_now_add=False)