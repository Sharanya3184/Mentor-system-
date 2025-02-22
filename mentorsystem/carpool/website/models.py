from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from datetime import date
# Create your models here.


class Student(models.Model):
    usern = models.OneToOneField(User, on_delete=models.CASCADE, max_length=80, unique=True, blank=True, default=None)
    fname = models.CharField(max_length=80, blank=True)
    email = models.EmailField(max_length=80, unique=True)
    password = models.CharField(max_length=200, default='default_password')
    gender = models.CharField(max_length=20)
    mobile = models.CharField(max_length=11, null=False)
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    state = models.CharField(max_length=100, null=False)
    college = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(max_length=200, null=True, blank=True)
    field_of_study = models.CharField(max_length=200, null=True, blank=True)
    graduation_year = models.CharField(max_length=4, null=True, blank=True)
    current_status = models.CharField(max_length=100, null=True, blank=True)
    company_name = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=200, null=True, blank=True)
    languages = models.CharField(max_length=500, null=True, blank=True)


    def __str__(self):
        return str(self.fname)

    from django.db import models
    from django.contrib.auth.models import User

    from django.db import models
    from django.contrib.auth.models import User

class Mentor(models.Model):
    usern = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, blank=True, default=None)
    fname = models.CharField(max_length=80, blank=True)
    email = models.EmailField(max_length=80, unique=True)
    password = models.CharField(max_length=200,
                                    default='default_password')  # Consider using Django's User model for passwords
    mobile = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, default='Unknown')
    city = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    role = models.CharField(max_length=200, null=True, blank=True)
    year_of_experience = models.CharField(max_length=50, null=True, blank=True)
    languages_spoken = models.CharField(max_length=500, null=True, blank=True)
    services = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)

    def __str__(self):
        return str(self.fname)


class ContactUs(models.Model):
    name=models.CharField(max_length=80)
    email=models.EmailField(max_length=80, unique=True, blank=False)
    phone=models.CharField(max_length=11, null=False, blank=True)
    msg=models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CalendarData(models.Model):
    day = models.CharField(max_length=20)
    checkbox = models.BooleanField(default=False)
    from_time = models.TimeField(null=True, blank=True)
    to_time = models.TimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    username = models.CharField(max_length=150, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    @property
    def from_time_formatted(self):
        return self.from_time.strftime('%I:%M %p') if self.from_time else ''

    @property
    def to_time_formatted(self):
        return self.to_time.strftime('%I:%M %p') if self.to_time else ''

    def __str__(self):
        return f"{self.username} - {self.day} - {self.from_time_formatted} to {self.to_time_formatted}"
class DeletedSchedule(models.Model):
    user_id = models.IntegerField(default=1)  # Set a default value, ensure it matches your setup
    day = models.CharField(max_length=20)
    from_time = models.TimeField()
    to_time = models.TimeField()
    username = models.CharField(max_length=150, default='default_username')  # Add a default value
    deleted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.day} - {self.from_time} to {self.to_time} (Deleted at: {self.deleted_at})"

class Service(models.Model):
    title = models.CharField(max_length=200)
    duration = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date = models.DateField(default=date.today)  # Ensure this field exists

    def __str__(self):
        return self.title

class Transaction(models.Model):
    service_title = models.CharField(max_length=255)
    service_duration = models.IntegerField()
    service_amount = models.DecimalField(max_digits=10, decimal_places=2)
    selected_day = models.CharField(max_length=50)
    selected_date = models.CharField(max_length=50)
    selected_time = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=50, default='success')
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=150,default='default')  # Adding the username field
    driver_username = models.CharField(max_length=150,default='default')  # Adding the driver's username field

    def __str__(self):
        return f'{self.service_title} for {self.username} on {self.selected_day} at {self.selected_time}'

