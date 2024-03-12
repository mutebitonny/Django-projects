from travelapp.views import *
#from django.contrib.auth import views as auth_views
# from django.conf.urls import url

from django.urls import re_path as url, include

urlpatterns=[
    url(r'^home/', home),
    url(r'^login/',login),
    url(r'^logout/',logout),
    url(r'^auth/',auth_user_view),
    url(r'^signup/',signup),
	url(r'^adduserdata/',adduserdata),
    url(r'^ticketbooking/',ticketbooking),
    url(r'^booking_packages/',booking_packages),
	url(r'^addbooking/',add_booking_data),
	url(r'^history/', booking_history),
	url(r'^delete/',delete),
	# url(r'^addfeedback/',addfeedback),
    url(r'^GetAmount/',GetAmount),
	url(r'^makepayment/',MakePayment),
	url(r'^bill/',bill),
]