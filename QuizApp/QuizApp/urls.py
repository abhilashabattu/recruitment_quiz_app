"""
URL configuration for QuizApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from quiz.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'),
     path('login/', signIn),
    path('register/', signUp),
    path('logout/', logout_view),
    
    
    
     path('quiz/<uuid:quiz_id>/sent/', view_sent_invites, name='view_sent_invites'),

    

    path('custom_quiz/', custom_quiz, name='custom_quiz'),
    path('generate_quiz/', generate_quiz, name='generate_quiz'),
    path('invite_candidates/', invite_candidates, name='invite_candidates'),
    path('view_sent_invites/', view_sent_invites, name='view_sent_invites'),
   
    path('quiz_invitations/', quiz_invitations, name='quiz_invitations'),
   

     path('quiz/register/<uuid:quiz_id>/', quiz_registration, name='quiz_register'),
    path('take-quiz/<uuid:quiz_id>/', take_quiz, name='take_quiz'),
     path('quiz-instructions/<uuid:quiz_id>/', quiz_instructions, name='quiz_instructions'),
    path('quiz/start/<uuid:quiz_id>/',take_quiz, name='take_quiz'),

    path('submit-quiz/<uuid:quiz_id>/', submit_quiz, name='submit_quiz'),
    path('final-submit/<uuid:quiz_id>/', final_submit, name='final_submit'),
      path('save-progress/', save_progress, name='save_progress'),
    path('quiz-success/<uuid:quiz_id>/', quiz_success, name='quiz_success'),
    
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
