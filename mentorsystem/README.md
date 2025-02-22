# Peer-to-Peer-Carpooling

The project is created using  HTML, CSS, JavaScript, Python, Django and MySQL. 

# Home Page
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/1ff01920-17a4-4ce5-8a0e-de7b2f26aba0)


# Home Page
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/15d49f14-4368-426c-a6bc-0e999d9ea00d)


# Registration Page
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/0a7ca281-bf66-477d-af32-01194de97023)


# Login Page
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/d2c30fac-7055-41da-9002-13f1542e1267)


# Contact Us Page
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/d0b941b3-b94f-4477-b0c4-303fbe596438)


# Dashboard Page
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/8d33dfc5-9752-40da-a7e3-e15228585234)


# Search Car Page
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/c1f68488-b9c3-4dba-a04d-224d8e8dc56e)


# Searched Cars according to dates and cities
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/cd7fed28-2d66-4561-a10e-be0ab3c4d57b)


# Car Booking Details
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/c20cc281-1d99-417c-bb2b-503f5181840e)


# Car Booked Successfully
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/37eeafe0-332f-421c-a81c-50e93d4fa331)


# All Cars Page
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/21c02b47-f7b5-4a5b-9e6c-5eb66554e5a3)


# User Added Car Page(My Cars)
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/735123a5-d19e-4f3e-b992-2eef6d82fdf1)


# Customer Bookings Page
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/cd32c77d-1b11-4c1e-b4fd-6558db0c450a)


# Add Car Details Page
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/04eaaddb-9d9f-435b-b520-f9f6551178d2)


# Change Password Page
![image](https://github.com/prachik26/Peer-to-Peer-Carpooling/assets/83691953/c0eebf8a-1158-4e71-b9dc-3c9c1b950a21)



For the project to run, we need to install Python 3.8 version with MySQL's latest version.
The IDE used for the project is VS Code.
Steps for running the project:
1. Open the Peer-to-Peer Carpooling folder in VS Code.
2. Create an environment for the project by opening command prompt in the VS Code and run the following commands for activating the environment:
   * python -m venv env
   * .\env\Scripts\activate
3. After running these commands, the environment will be activated. Now we have install the requires libraries of python. So run the following pip install commands:
   * pip install django
   * pip install requests
   * pip install cryptography
   * pip install mysql-connector-python
   * pip install pillow
   * pip install pymysql
4. After installing all these libraries, we need to create a database in mysql and give it's details to the settings.py file in Peer-to-Peer Carpooling>carpool>carpool folder. The same details should be added in the views.py file in Major 2>carpool>website folder.
5. Ater creating the database, run the following commands to run the server of Django:
   * cd carpool
   * python manage.py makemigrations
   * python manage.py sqlmigrate website 0001
   * python manage.py sqlmigrate website 0002
   * python manage.py sqlmigrate website 0003
   * python manage.py sqlmigrate website 0004
   * python manage.py sqlmigrate website 0005
   * python manage.py migrate
   * python manage.py runserver                //This command runs the Django server and for closing the server 'Ctrl+C' should be pressed in the command prompt terminal of VS Code.
6. The above commands will create the required tables in the database details provided by you and then run the server i.e. http://127.0.0.1:8000/ in your chrome browser.
7. All the images of the web application gets saved in the static folder, which contains of images, javascript files, and css files. All the images of cars that are uploaded in the ADD JOURNEY DETAILS page are saved in the static>images>cars folder by default.
8. All the html pages are present in templates folder.
