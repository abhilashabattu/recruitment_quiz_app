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
# ADMIN PORTAL
![Project and 5 more pages - Personal - Microsoft_ Edge 2025-07-05 14-31-11 (1)](https://github.com/user-attachments/assets/c1f92fce-2614-4f9d-b945-858469d38aa8)

# CANDIDATE PORTAL
![Screenshot 2025-07-05 155338](https://github.com/user-attachments/assets/73f1a54f-979c-46c1-a86e-0b1ed34ec3ac)
![Screenshot 2025-07-05 155327](https://github.com/user-attachments/assets/ec0b627e-ebd6-4506-aab1-29dbcb125afd)
![Screenshot 2025-07-05 155036](https://github.com/user-attachments/assets/b6d75442-6b61-4720-b0be-49f50f52b3ff)
![Screenshot 2025-07-05 155018](https://github.com/user-attachments/assets/8605769b-9700-4274-a845-16053a0820ec)
![Screenshot 2025-07-05 154818](https://github.com/user-attachments/assets/ec45e1cc-e4a0-4424-9038-8236c3b07ba2)
![Screenshot 2025-07-05 154802](https://github.com/user-attachments/assets/9aba8f22-4a9e-4311-b392-7557cd3d0627)

