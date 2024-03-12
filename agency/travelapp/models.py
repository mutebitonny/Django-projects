from django.db import models
from django.contrib.auth.models import User
# from travelapp.models import TMSUser

# Create your models here.
class RUser(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	mobileNo = models.CharField(max_length=10)

class PackageDetails(models.Model):
	packagename = models.CharField(max_length=20,primary_key=True)
	amount = models.CharField(max_length=10)

class RBooking(models.Model):
	booking_id=models.CharField(max_length=6,primary_key=True)
	ruser = models.ForeignKey(RUser,on_delete=models.CASCADE,null=True)
	location = models.CharField(max_length=20)
	destination = models.CharField(max_length=20)
	package = models.ForeignKey(PackageDetails,on_delete=models.CASCADE,null=True)
	departure_date = models.DateField()
	no_of_people = models.PositiveIntegerField(default=0)
	amount=models.PositiveIntegerField()

class addfeedback(models.Model):
	ruser = models.ForeignKey(RUser, on_delete=models.CASCADE, null=True)
	addfeedback=models.TextField(max_length=200)

class RPayment(models.Model):
    payment_id=models.CharField(max_length=6,primary_key=True)
    ruser = models.ForeignKey(RUser, on_delete=models.CASCADE, null=True)
    amount=models.PositiveIntegerField()
    mode=models.CharField(max_length=25)
