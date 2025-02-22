from django.urls import path
from website import views
from .views import service_create  # Import the service_create function
from .views import service_create, service_detail, payment, payment_verification




urlpatterns=[
    #path('payment/', payment, name='payment'),
    #path('payment/verification/', payment_verification, name='payment_verification'),
    path('',views.home, name="home"),
    path('bookings/', views.bookings_view, name='bookings'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('changepassword/', views.Change, name="changepassword"),
    path('contact/', views.Contactus, name="contact"),
    path('dashboard/', views.dash, name="dashboard"),
    path('delete-schedule/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    path('login/', views.LoginUser, name="login"),
    path('logout/',views.logout_user, name="logout"),
    path('myaccount', views.MyAccount,name="myaccount"),
    path('mybookings/', views.MyBookings, name="mybookings"),
    path('page/<str:username>/', views.page, name='page'),
    path('payment-verification/', payment_verification, name='payment_verification'),
    path('payment/<int:pk>/', payment, name='payment'),
    path('register/', views.Register, name="register"),
    path('searchmymentor/', views.Search, name="searchmymentor"),
    path('service/', views.service_view, name='service'),
    path('service/<int:pk>/', views.service_detail, name='service_detail'),
    path('service/create/', service_create, name='service_create'),
    path('testimonial/', views.testimonial_view, name='testimonial'),


    

]