from django.db import models
from django.contrib.auth.models import User

class Record(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    phone=models.CharField(max_length=10)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    zipcode=models.CharField(max_length=6)

    def __str__(self) -> str:
        return (f"{self.first_name} {self.last_name} ")

class Communication(models.Model):
    customer = models.ForeignKey(Record, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.TextField()   
