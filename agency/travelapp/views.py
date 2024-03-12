from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from .models import RUser, RBooking, addfeedback, PackageDetails, RBooking, RPayment
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib.sessions.models import Session
from django.utils.crypto import get_random_string
from django.utils.timezone import datetime


# Create your views here.
def signup(request):
    c={}
    c.update(csrf(request))
    return render(request,'signup.html',c)

def adduserdata(request):
	rusername=request.POST.get('username','')
	passwd=request.POST.get('password','')
	cpasswd=request.POST.get('cpassword','')
	emailid=request.POST.get('emailid','')
	mobno=request.POST.get('mobileNo','')
	if(passwd==cpasswd):
		if(len(passwd)>8):
			r=User.objects.create_user(username=rusername,password=passwd,email=emailid)
			print(r)
			r.RUser = RUser(user=r,mobileNo=mobno)
			r.RUser.save()
			r.save()
			return HttpResponseRedirect('/travelapp/login/')
		else:
			return render(request,'signup.html',{"error1":"Password length cannot be less than 8"})
	else:
		return render(request,'signup.html',{"error2":"Password doesn't match. Enter right password"})

def home(request):
	c={}
	c.update(csrf(request))
	request.session['temp'] = "xyz"
	c['packages'] = PackageDetails.objects.all()
	return render(request,'home.html',c)

def login(request):
		c={}
		c.update(csrf(request))
		return render(request,'login.html',c)

def auth_user_view(request):
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	user = auth.authenticate(username=username, password=password)
	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/travelapp/home/')
	else:
		return render(request,'login.html',{"error":"Invalid Username or Password"})

def logout(request):
	auth.logout(request)
	return render(request, 'logout.html')

def booking_packages(request):
    c={}
    c.update(csrf(request))
    request.session['temp'] = "xyz"
    c['packages'] = PackageDetails.objects.all()
    return render(request,'booking_packages.html',c)

@login_required
def ticketbooking(request):
	c={}
	c.update(csrf(request))
	request.session['temp']="xyz"
	request.session['full_name']=request.user.username

	c['packages'] = PackageDetails.objects.all()
	c['randomid']=get_random_string(length=4)
	return render(request,'ticketbooking.html',c)

@login_required
def add_booking_data(request):
	bookingid=request.POST.get('bookingid','')
	location1=request.POST.get('location','')
	destination1=request.POST.get('destination','')
	package1=request.POST.get('package','')
	date=request.POST.get('date','')
	no_of_people=request.POST.get('no_of_people','')
	amt= int(PackageDetails.objects.get(packagename=package1).amount)
	total_amount= int(no_of_people) * (amt)
	request.session['total_amount']=total_amount
	s=RBooking(booking_id=bookingid,amount=total_amount,location=location1,destination=destination1,
				 package=PackageDetails.objects.get(packagename=package1),departure_date=date,
				 no_of_people=no_of_people,ruser=RUser.objects.get(user=request.user))
	if(location1!=destination1):
		s.save()
		request.session['package']=package1
		request.session['nop'] = no_of_people
		request.session['location']=location1
		request.session['destination']=destination1
		request.session['date']=date
		return HttpResponseRedirect('/travelapp/GetAmount/')
	else:
		request.session['error3']="Your source and destination can't be same"
		return HttpResponseRedirect('/travelapp/ticketbooking/')

@login_required
def booking_history(request):
	request.session['temp']="abc"
	c={}
	c['today']=datetime.today().date()
	c['bookings'] = RBooking.objects.filter(ruser=request.user.ruser)
	return render(request,'booking_history.html',c)
def delete(request):
	RBooking.objects.filter(booking_id=request.POST.get('cancel')).delete()
	return HttpResponseRedirect('/travelapp/history/')

@login_required
def addfeedback(request):
	# return render(request,'feedback.html')
    # def addfeedback(request):
	addfeedback=request.POST.get('addfeedback','')
	f=addfeedback(ruser=RUser.objects.get(user=request.user),addfeedback=addfeedback)
	f.save()
	return render(request,'home.html')

@login_required
def GetAmount(request):
    return render(request,'amount.html')

@login_required
def MakePayment(request):
    c={}
    c.update(csrf(request))
    request.session['mode']=request.POST.get('mode','')
    return render(request,'payment.html',c)

@login_required
def bill(request):
    c={}
    paymentid=get_random_string(length=4)
    mode=request.session.get('mode')
    amount=request.session.get('total_amount')
    p=RPayment(payment_id=paymentid,amount=amount,mode=mode,ruser=RUser.objects.get(user=request.user))
    p.save()
    return render(request,'bill.html', c)

