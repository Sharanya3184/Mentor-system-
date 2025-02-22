#from dateutil.parser import parse, ParserError
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import make_aware
from django.views import View
# import mysql.connector as sql
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from requests import request
from django.contrib.auth.hashers import make_password
from .models import Student, ContactUs, Mentor, CalendarData, DeletedSchedule, Service, \
    Transaction
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CalendarData  # Import your CalendarData model
from django.contrib import messages
from django.db.models import Max
import base64
from django.core.files.base import ContentFile
import razorpay
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import base64
from PIL import Image
from io import BytesIO

import hmac
import hashlib
from datetime import datetime, timedelta
from .models import Service, CalendarData

from collections import defaultdict


# Create your views here.

# Home page
def home(request):
    if request.user.is_authenticated:
         user_id = request.user.id
         if Student.objects.filter(usern=user_id).exists():
            userType = 'Student'
         elif Mentor.objects.filter(usern=user_id).exists():
            userType = 'Mentor'
         context = {'userType': userType}
         return render(request, "home.html", context)
    return render(request, "home.html")

# Function to help login the user and open dashboard
def LoginUser(request):
    if request.method == "GET":
        return render(request, "login.html")

    if request.method == "POST":
        usern = request.POST.get('usern')  # Use get() to safely get form input
        password = request.POST.get('password')

        try:
            user = authenticate(username=usern, password=password)
            if user is not None:
                login(request, user)

                # Check if the user is a Customer
                if Student.objects.filter(usern=user).exists():
                    return redirect('searchmymentor')

                # Check if the user is a Driver
                elif Mentor.objects.filter(usern=user).exists():
                    return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password!")
        except User.DoesNotExist:
            messages.error(request, "Invalid username!")

    return redirect('login')


def Register(request):
    if request.method == 'GET':
        return render(request, "registration.html")

    if request.method == 'POST':
        if 'usern' in request.POST:  # User registration
            # Extract basic user information
            usern = request.POST['usern']
            fname = request.POST['fname']
            email = request.POST['email']
            password = request.POST['password']
            mobile = request.POST['mobile']
            gender = request.POST['gender']
            address = request.POST['address']
            city = request.POST['city']
            state = request.POST['state']
            # Extract additional user information
            college = request.POST['college']
            degree = request.POST['degree']
            field_of_study = request.POST['field_of_study']
            graduation_year = request.POST['graduation_year']
            languages_user = request.POST.getlist('languages_user')
            current_status = request.POST['current-status']
            company_name = request.POST.get('company-name', None)
            role = request.POST.get('role', None)

            # Join the selected languages into a single string
            languages_str = ','.join(languages_user)

            # Print statements to check extracted data
            print("Username:", usern)
            print("Full Name:", fname)
            print("Email:", email)
            print("Password:", password)  # Note: Passwords should not be printed in production
            print("Mobile:", mobile)
            print("Gender:", gender)
            print("Address:", address)
            print("City:", city)
            print("State:", state)
            print("College:", college)
            print("Degree:", degree)
            print("Field of Study:", field_of_study)
            print("Graduation Year:", graduation_year)
            print("Languages Spoken:", languages_str)
            print("Current Status:", current_status)
            print("Company Name:", company_name)
            print("Role:", role)

            # Validate mobile number
            if len(mobile) != 10 or not mobile.isdigit():
                messages.warning(request, "The phone number provided is not valid!")
                return redirect('register')

            try:
				 # Create user object
                user = User.objects.create_user(username=usern, email=email, password=password)
                user.save()
                # Create customer object
                cust = Student.objects.create(
                    usern=user,
                    fname=fname,
                    email=email,
                    mobile=mobile,
                    gender=gender,
                    address=address,
                    city=city,
                    state=state,
                    college=college,
                    degree=degree,
                    field_of_study=field_of_study,
                    graduation_year=graduation_year,
                    current_status=current_status,
                    company_name=company_name,
                    role=role,
                    languages=languages_str
                )
                # Save customer object
                cust.save()
                messages.success(request, "Account created successfully!")
                return redirect('login')
            except IntegrityError:
                messages.warning(request, "Account already exists!")
                return redirect('register')

        elif 'usern_driver' in request.POST:  # Driver registration
            usern = request.POST['usern_driver']
            fname = request.POST['fname_driver']
            email = request.POST['email_driver']
            password = request.POST['password_driver']
            mobile = request.POST['mobile_driver']
            address = request.POST['address_driver']
            gender = request.POST['gender_driver']
            state = request.POST['state_driver']
            city = request.POST['city_driver']
            role = request.POST['role']
            year_of_experience = request.POST['year-of-experience']
            languages_driver = request.POST.getlist('languages_driver')
            services = request.POST.getlist('services_driver[]')
            description = request.POST['description_driver']
            cropped_image_data = request.POST.get('cropped_image_data')

            # Join the selected languages into a single string
            languages_str = ','.join(languages_driver)

            print("Username:", usern)
            print("Full Name:", fname)
            print("Email:", email)
            print("Password:", password)  # Note: Passwords should not be printed in production
            print("Mobile:", mobile)
            print("Address:", address)
            print("Gender:", gender)
            print("State:", state)
            print("City:", city)
            print("Role:", role)
            print("Year of Experience:", year_of_experience)
            print("Languages Spoken:", languages_str)
            print("Services:", services)
            print("Description:", description)

        if len(mobile) != 10 or not mobile.isdigit():
            messages.warning(request, "The phone number provided is not valid!")
            return redirect('register')

        try:
            user = User.objects.create_user(username=usern, email=email, password=password)
            user.save()
            driver = Mentor.objects.create(
                usern=user,
                fname=fname,
                email=email,
                mobile=mobile,
                address=address,
                gender=gender,
                state=state,
                city=city,
                role=role,
                year_of_experience=year_of_experience,
                languages_spoken=languages_str,
                services=services,
                description=description
            )
            cropped_image_data = request.POST['cropped_image_data']
            if cropped_image_data:
                format, imgstr = cropped_image_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name=f'{usern}_profile_picture.{ext}')
                driver.profile_picture.save(data.name, data)
                driver.save()
            else:
                img_data = None
            messages.success(request, "Account created successfully!")
            return redirect('login')
        except IntegrityError:
            messages.warning(request, "Account already exists!")
            return redirect('register')

    return render(request, "registration.html")




def generate_time_intervals():
    current_time = datetime.strptime("12:00 AM", "%I:%M %p")
    time_strings = []
    for _ in range(96):
        time_strings.append(current_time.strftime("%I:%M %p"))
        current_time += timedelta(minutes=15)
    return time_strings


@login_required
def calendar_view(request):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    times = generate_time_intervals()
    context = {}

    if request.method == 'POST':
        username = request.user.username
        new_entries = []
        has_overlap = False

        for day in days:
            checkbox = request.POST.get(f'{day.lower()}_checkbox', False) == 'on'
            if checkbox:
                from_times = request.POST.getlist(f'{day.lower()}_from_time')
                to_times = request.POST.getlist(f'{day.lower()}_to_time')

                for i in range(len(from_times)):
                    from_time_str = from_times[i]
                    to_time_str = to_times[i]
                    from_time = datetime.strptime(from_time_str, "%I:%M %p")
                    to_time = datetime.strptime(to_time_str, "%I:%M %p")

                    if to_time == from_time:
                        messages.error(request,
                                       f"From time and To time cannot be the same")
                        has_error = True
                        break

                    if to_time <= from_time:
                        to_time += timedelta(days=1)

                    new_entry = {
                        'day': day,
                        'from_time': from_time,
                        'to_time': to_time
                    }

                    # Check for overlap with existing new entries
                    for entry in new_entries:
                        if entry['day'] == day:
                            if (entry['from_time'] < to_time and from_time < entry['to_time']):
                                has_overlap = True
                                messages.error(request,
                                               f"Time overlaps with another slot")
                                break

                    new_entries.append(new_entry)
                    if has_overlap:
                        break

        # Save new entries if no overlap is found
        if not has_overlap:
            CalendarData.objects.filter(username=username, is_deleted=False).update(is_deleted=True)
            print("has_overlap ", new_entries)
            for entry in new_entries:
                try:
                    CalendarData.objects.create(
                        day=entry['day'],
                        checkbox=True,
                        from_time=entry['from_time'].time(),
                        to_time=entry['to_time'].time(),
                        username=username
                    )
                except Exception as e:
                    messages.error(request, f"Error: {e}")

    # Refresh latest schedule data after adding new entries
    context = buildContextForSchedules(load_latest_schedule(request.user.username, days), days, times)
    return render(request, "calendar.html", context)


def buildContextForSchedules(schedule_data, days, times):
    return {
        'schedule_data': schedule_data,
        'days': days,
        'times': times
    }


def load_latest_schedule(username, days):
    latest_schedule_data = []
    try:
        for day in days:
            schedule_entries = list(CalendarData.objects.filter(
                username=username, day=day, is_deleted=False
            ))
            latest_schedule_data.extend(schedule_entries)
        print("latest_schedule_data ", latest_schedule_data)
    except CalendarData.DoesNotExist as e:
        messages.error(request, f"Error: {e}")
    return latest_schedule_data


@login_required
def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(CalendarData, id=schedule_id)
    DeletedSchedule.objects.create(
        day=schedule.day,
        from_time=schedule.from_time,
        to_time=schedule.to_time,
        user_id=schedule.user.id,  # Store user ID
        username=schedule.user.username  # Store username
    )
    schedule.delete()
    # messages.success(request, 'Schedule deleted successfully')
    return redirect('calendar')


@login_required
def Search(request):
    if request.method == "GET":
        search_term = request.GET.get('search_term', '').strip()
        year_of_experience = request.GET.get('year_of_experience', '').strip()

        mentors = Mentor.objects.all()  # Start with all mentors

        if search_term:
            terms = search_term.split()  # Split input into individual terms (roles)
            search_conditions = Q()

            for term in terms:
                # Add conditions to match each term against relevant fields
                term_conditions = (Q(usern__icontains=term) |
                                   Q(role__icontains=term) |
                                   Q(services__icontains=term) |
                                   Q(languages_spoken__icontains=term))
                search_conditions |= term_conditions  # Combine with OR for each term

            # Filter mentors based on combined search conditions
            mentors = mentors.filter(search_conditions)

        if year_of_experience:
            if year_of_experience == "greater_than_2":
                mentors = mentors.filter(year_of_experience__gt=2)
            else:
                mentors = mentors.filter(year_of_experience=year_of_experience)

        # Process mentors to clean up services for template display
        for mentor in mentors:
            if mentor.services:
                # Clean up services: strip square brackets, split by comma, strip quotes
                services = mentor.services.strip("[]").split(",")
                cleaned_services = [service.strip().strip('"\'') for service in services]
                mentor.services = cleaned_services

        # Process each mentor to split languages_spoken
        for mentor in mentors:
            if mentor.languages_spoken:
                mentor.languages_spoken = mentor.languages_spoken.split(',')

        # Collect unique filter items
        unique_roles = set(mentor.role for mentor in mentors if mentor.role)
        unique_years_of_experience = set(mentor.year_of_experience for mentor in mentors if mentor.year_of_experience)
        unique_languages_spoken = set(
            language for mentor in mentors if mentor.languages_spoken for language in mentor.languages_spoken)
        unique_services = set(service for mentor in mentors if mentor.services for service in mentor.services)

        return render(request, 'search.html', {
            'mentors': mentors,
            'search_term': search_term,
            'year_of_experience': year_of_experience,
            'unique_roles': unique_roles,
            'unique_years_of_experience': unique_years_of_experience,
            'unique_languages_spoken': unique_languages_spoken,
            'unique_services': unique_services,
        })

    return render(request, "search.html")


# Function to show logged in user's account details
@login_required(login_url='login')
def page(request, username):
    try:
        # Attempt to fetch Customer by username
        cust = Student.objects.get(usern__username=username)
        context = {'cust': cust}
        return render(request, "page.html", context)
    except Student.DoesNotExist:
        try:
            # Attempt to fetch Driver by username
            driver = Mentor.objects.get(usern__username=username)
            context = {
                'user_type': 'driver',
                'name': driver.fname,
                'description': driver.description,
                'profile_picture': driver.profile_picture.url if driver.profile_picture else None,
                'services': Service.objects.filter(user=driver.usern)  # Fetch all services for drivers
            }
            return render(request, "page.html", context)
        except Mentor.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('home')


@login_required
def service_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        duration = request.POST.get('duration')
        amount = request.POST.get('amount')

        service = Service(title=title, duration=duration, amount=amount, user=request.user)
        service.save()

        messages.success(request, 'Service successfully saved!')

        return redirect('service_create')

    services = Service.objects.filter(user=request.user)  # Filter services by the logged-in user

    return render(request, 'service.html', {'services': services})


@login_required
def service_delete(request, service_id):
    service = get_object_or_404(Service, id=service_id, user=request.user)  # Ensure the service belongs to the user
    if request.method == 'DELETE':
        service.delete()
        messages.success(request, 'Service deleted successfully')
        return JsonResponse({'message': 'Service deleted successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required(login_url='login')
def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    amount_in_paise = int(service.amount * 100)

    # Fetch the driver based on the service user (assuming user in Service model)
    driver = Mentor.objects.get(usern=service.user)

    # Fetch calendar data based on the driver's user
    calendar_data = CalendarData.objects.filter(username=driver.usern.username, is_deleted=False)
    print(f'calendar data--> {calendar_data}')

    # Create a list of dates for the next 4 weeks
    current_date = datetime.now()
    dates_list = [(current_date + timedelta(days=i)).strftime("%Y%m%d") for i in range(28)]
    print(f'dates_list--> {dates_list}')

    # Create a dictionary to hold formatted calendar data
    grouped_calendar_data = {}
    for calendar in calendar_data:
        for date in dates_list:
            day_name = datetime.strptime(date, "%Y%m%d").strftime("%a")
            if day_name == calendar.day[:3]:  # Match the day name
                if date in grouped_calendar_data:
                    existing_from_time = grouped_calendar_data[date]['from_times']
                    from_time = f'{existing_from_time}|{calendar.from_time.strftime("%I:%M %p")}'
                else:
                    from_time = calendar.from_time.strftime("%I:%M %p")

                grouped_calendar_data[date] = {
                    'day': calendar.day[:3],
                    'from_times': from_time,
                    'pretty_date': datetime.strptime(date, "%Y%m%d").strftime("%d %b")
                }

    print(f'Calculated grouped_calendar_data :: {grouped_calendar_data}')
    print(f'len(grouped_calendar_data):: {len(grouped_calendar_data)}')
    if len(grouped_calendar_data) < 1:
        context = {
            'service': service,
            'amount_in_paise': amount_in_paise,
            'calendar_data': grouped_calendar_data,
            'user': request.user,
            'driver_username': driver.usern.username,
            'mentor_availability': False
        }
        return render(request, 'service_detail_page.html', context)
    grouped_calendar_data = dict(sorted(grouped_calendar_data.items()))  # sort the dates in ascending order

    context = {
        'service': service,
        'amount_in_paise': amount_in_paise,
        'calendar_data': grouped_calendar_data,
        'user': request.user,
        'driver_username': driver.usern.username,
        'mentor_availability': True
    }

    print(f'context in service_detail_page :: {context}')

    return render(request, 'service_detail_page.html', context)

# Function to help user contact the admin
def Contactus(request):
    if request.method == "GET":
        return render(request, "contact.html")

    if request.method == "POST":
        # m=sql.connect(host="localhost", user="root", passwd="Web@123456", database='carpooling')
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        msg = request.POST['msg']
        if len(phone) != 10 or phone.isdigit() == False:
            messages.warning(request, "The phone number provided is not 10 digits!")
        elif phone.startswith(('1', '2', '3', '4', '5', '0')):
            messages.warning(request, "The phone number provided is not valid!")
        else:
            contact_us = ContactUs.objects.create(name=name, email=email, phone=phone, msg=msg)

            # save the contact details in database
            # print(request.user)
            # customer = Customer.objects.get(usern=user_name)
            #    contact_us = ContactUs.objects.create(name=name, email=email, phone=phone, msg=msg, cust=customer)
            # else:
            #    contact_us = ContactUs.objects.create(name=name, email=email, phone=phone, msg=msg, cust=None)

            # print(contact_us)
            contact_us.save()
            # m.commit()
            messages.success(request, "Thank you for contacting us, we will reach you soon.")

        return render(request, "contact.html")




# Function to show dashboard to the logged in users
def dash(request):
    if request.user.is_authenticated:
        print(f'In dash function:: {dict(request.POST.items())}')
        print(f'In dash function:: {request.user}')
        return render(request, "dashboard.html")


@login_required
def bookings_view(request):

    transactions = Transaction.objects.filter(driver_username=request.user.username)

    # Get the current date and time, and make it timezone-aware
    now = datetime.now()
    now = make_aware(now)  # Ensure it's timezone-aware

    current_year = now.year

    # Separate transactions into completed and upcoming
    completed_bookings = []
    upcoming_bookings = []

    for transaction in transactions:
        try:
            # Parse date assuming current year and format "DD MMM"
            transaction_date_str = transaction.selected_date + f" {current_year}"
            booking_date = datetime.strptime(transaction_date_str, '%d %b %Y')
            booking_date = make_aware(booking_date)  # Ensure it's timezone-aware
        except ValueError:
            # Handle the case where the date format is incorrect
            booking_date = None

        if booking_date:
            if booking_date < now:
                completed_bookings.append(transaction)
            else:
                upcoming_bookings.append(transaction)
        else:
            # Handle cases where the date is not parseable
            print(f"Invalid date format for transaction: {transaction.selected_date}")

    context = {
        'completed_bookings': completed_bookings,
        'upcoming_bookings': upcoming_bookings,
    }

    return render(request, 'bookings.html', context)



def service_view(request):
    # Your logic for rendering the service page goes here

    services = Service.objects.filter(user=request.user)  # Filter services by the logged-in user
    context = {'services': services}

    return render(request, 'service.html', context)


def testimonial_view(request):
    # Add any logic you need here
    return render(request, 'testimonial.html')


# Function to show logged in user's bookings from the dashboard
#
@login_required
def MyBookings(request):
    # Filter transactions based on the logged-in user's username
    transactions = Transaction.objects.filter(username=request.user.username)

    # Get the current date and time, and make it timezone-aware
    now = datetime.now()
    now = make_aware(now)  # Ensure it's timezone-aware

    current_year = now.year

    # Separate transactions into completed and upcoming
    completed_bookings = []
    upcoming_bookings = []

    for transaction in transactions:
        try:
            # Parse date assuming current year and format "DD MMM"
            transaction_date_str = transaction.selected_date + f" {current_year}"
            booking_date = datetime.strptime(transaction_date_str, '%d %b %Y')
            booking_date = make_aware(booking_date)  # Ensure it's timezone-aware
        except ValueError:
            # Handle the case where the date format is incorrect
            booking_date = None

        if booking_date:
            if booking_date < now:
                completed_bookings.append(transaction)
            else:
                upcoming_bookings.append(transaction)
        else:
            # Handle cases where the date is not parseable
            print(f"Invalid date format for transaction: {transaction.selected_date}")

    context = {
        'completed_bookings': completed_bookings,
        'upcoming_bookings': upcoming_bookings,
    }

    return render(request, "mybooking.html", context)


# Function to show logged in user's account details
def MyAccount(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = request.user
            cust = Student.objects.get(usern=user)
            # print(cust)
            context = {'cust': cust}
            return render(request, "myaccount.html", context)

# Function to help logged in user to change password on change.html
def Change(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, "change.html")

    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            print(user)
            old_password = request.POST['old_password']
            print(old_password)
            new_password = request.POST['new_password']
            print(new_password)
            confirm_password = request.POST['confirm_password']
            print(confirm_password)
            usern = authenticate(request, username=user, password=old_password)
            print(usern)
            if usern is None:
                messages.error(request, 'The old password is incorrect!')
                return redirect('changepassword')

            if new_password != confirm_password:
                messages.error(request, 'The new password and confirm password does not match!')
                return redirect('changepassword')

            print(user.password)
            user.password = make_password(new_password)
            user.save()
            login(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('changepassword')
    return render(request, 'change.html')



def logout_user(request):
    if request.user.is_authenticated:
        # request.session.clear()
        # print('User is authenticated')
        logout(request)
    return redirect('home')


# Initialize Razorpay client
client = razorpay.Client(auth=('rzp_test_tsuNnuJYVpl9O8', 'N1CiBGN3MRVFQRq5rtYll9E5'))


@csrf_exempt
def payment(request, pk=None):
    try:
        if request.method == 'POST':
            data = request.POST
            service_title = data['service_title']
            service_duration = data['service_duration']
            service_amount = data['service_amount']
            selected_day = data['selected_day']
            selected_date = data['selected_date']  # Fetch the selected date
            selected_time = data['selected_time']
            username = data['username']
            driver_username = data['driver_username']

            # Debugging print statement
            print(f"Service Title: {service_title}")
            print(f"Service Duration: {service_duration}")
            print(f"Service Amount: {service_amount}")
            print(f"Selected Day: {selected_day}")
            print(f"Selected Date: {selected_date}")  # Print the selected date
            print(f"Selected Time: {selected_time}")
            print(f"Username: {username}")
            print(f"Driver Username: {driver_username}")
        else:
            service = get_object_or_404(Service, pk=pk)
            service_title = service.title
            service_duration = service.duration
            service_amount = service.amount
            selected_day = ''
            selected_date = ''  # Initialize with an empty string
            selected_time = ''
            username = ''
            driver_username = ''

        amount = int(float(service_amount) * 100)  # amount in paise
        currency = 'INR'
        payment_capture = '1'

        order = client.order.create({
            'amount': amount,
            'currency': currency,
            'payment_capture': payment_capture,
        })

        if request.method == 'POST':
            # Save the transaction info with a pending payment status
            Transaction.objects.create(
                service_title=service_title,
                service_duration=service_duration,
                service_amount=service_amount,
                selected_day=selected_day,
                selected_time=selected_time,
                selected_date=selected_date,  # Save the selected date
                payment_status='Pending',
                razorpay_order_id=order['id'],
                username=username,
                driver_username=driver_username
            )

        context = {
            'order_id': order['id'],
            'amount': amount / 100,  # Convert paise to rupees
            'currency': currency,
        }
        return render(request, 'payment_success.html', context)
    except razorpay.errors.BadRequestError as e:
        context = {'error': str(e)}
        return render(request, 'payment_failure.html', context)
    except Exception as e:
        context = {'error': 'Something went wrong'}
        return render(request, 'payment_failure.html', context)
@csrf_exempt
def payment_verification(request):
    if request.method == 'POST':
        try:
            data = request.POST
            params_dict = {
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            }

            print(f"Payment Verification Data: {params_dict}")

            # Verify the payment signature
            client.utility.verify_payment_signature(params_dict)

            # Update transaction status to success
            transaction = Transaction.objects.get(razorpay_order_id=data['razorpay_order_id'])
            transaction.razorpay_payment_id = data['razorpay_payment_id']
            transaction.razorpay_signature = data['razorpay_signature']
            transaction.payment_status = 'Success'
            transaction.save()

            print(f"Payment Success for Order ID: {data['razorpay_order_id']}")

            return JsonResponse({'status': 'Payment successful'})
        except razorpay.errors.SignatureVerificationError:
            print(f"Signature Verification Failed for Order ID: {data['razorpay_order_id']}")
            transaction = Transaction.objects.get(razorpay_order_id=data['razorpay_order_id'])
            transaction.payment_status = 'Failed'
            transaction.save()
            return JsonResponse({'status': 'Payment verification failed'}, status=400)
        except Exception as e:
            print(f"Exception: {str(e)}")
            return JsonResponse({'status': 'Something went wrong'}, status=500)

    return HttpResponse(status=405)