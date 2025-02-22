"Mentor-system using django code to set up in the terminal"
python -m venv env
.\env\Scripts\activate
pip install django
pip install requests
pip install cryptography
pip install mysql-connector-python
pip install pillow
pip install pymysql
pip install djangorestframework
pip install razorpay
pip install setuptools
pip install python_dateutil
cd carpool
python manage.py makemigrations
python manage.py sqlmigrate website 0001
python manage.py sqlmigrate website 0002
python manage.py sqlmigrate website 0003
python manage.py sqlmigrate website 0004
python manage.py sqlmigrate website 0005
python manage.py migrate
python manage.py runserver   
