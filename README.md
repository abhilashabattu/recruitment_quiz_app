# recruitment_quiz_app
# Quiz Application

A Django-based web application that allows users to create and take quizzes on various programming topics (Java, Python, CSS, HTML, JavaScript, jQuery). Features include user authentication, quiz creation, candidate invitation system, and result tracking.

## Features

- User authentication (login/registration)
- Multiple quiz domains (Java, Python, CSS, HTML, JavaScript, jQuery)
- Custom quiz creation with difficulty levels
- Candidate invitation system via email
- Quiz progress saving
- Detailed results and scoring
- Responsive design

## Technologies Used

- Python 3.x
- Django 5.2
- HTML/CSS/JavaScript
- Bootstrap (for frontend styling)
- SMTP (for email functionality)


### Prerequisites

1. Python 3.x installed
2. MySQL server installed and running
3. Git (optional)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/quiz-app.git
   cd quiz-app 

2. **Create and activate a virtual environment**
   	python -m venv venv
	# On Windows
	venv\Scripts\activate
	# On macOS/Linux
	source venv/bin/activate 

3. **Install dependencies**
	pip install -r requirements.txt
4. **Database Setup**

	-Create a MySQL database named quiz_db
	-Update database settings in settings.py if needed:
		DATABASES = {
 		   'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'quiz_db',
        	'USER': 'your_mysql_username',
	        'PASSWORD': 'your_mysql_password',
        	'HOST': 'localhost',
	        'PORT': '3306',
    			}
		}
5. **Apply Migrations**
	python manage.py migrate

6. **Create a superuser (admin)**
	python manage.py createsuperuser

7. **Set up email configuration (optional)**
	-Update these settings in settings.py for email functionality:
		EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
		EMAIL_HOST = 'smtp.gmail.com'
		EMAIL_PORT = 587
		EMAIL_USE_TLS = True
		EMAIL_HOST_USER = 'your_email@gmail.com'
		EMAIL_HOST_PASSWORD = 'your_app_password'  # For Gmail, use an App Password
		DEFAULT_FROM_EMAIL = 'your_email@gmail.com'

8. **Run the development server**
	python manage.py runserver

9. **Access the application**
	Open your browser and go to http://127.0.0.1:8000


### Project Structure
	QuizApp/
	├── quiz/                      # Main app directory
	│   ├── migrations/            # Database migrations
	│   ├── templates/             # HTML templates
	│   ├── admin.py               # Admin configuration
	│   ├── apps.py                # App configuration
	│   ├── forms.py               # Form definitions
	│   ├── models.py              # Database models
	│   ├── urls.py                # App URL routing
	│   └── views.py               # View functions
	├── QuizApp/                   # Project settings
	│   ├── settings.py            # Project settings
	│   ├── urls.py                # Main URL routing
	│   └── wsgi.py                # WSGI configuration
	├── manage.py                  # Django management script
	└── requirements.txt           # Python dependencies

### Usage
For Quiz Creators:

   -Register or login

   -Select domains and difficulty levels

   -Generate a quiz

   -Invite candidates via email

   -View results

For Candidates:

   -Click on the invitation link received via email

   -Register or login

   -Take the quiz

   -View results after submission



---
![Project and 5 more pages - Personal - Microsoft_ Edge 2025-07-05 14-31-11](https://github.com/user-attachments/assets/51f7f059-c70b-4949-bf78-26f159f58760)
