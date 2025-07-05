import json
import random
from django.http import Http404, JsonResponse
from django.shortcuts import render,redirect,HttpResponse
from django.shortcuts import get_object_or_404
from django.template.defaulttags import register
from quiz.models import JavaQuestion,PythonQuestion,CSSQuestion, HTMLQuestion, JavaScriptQuestion,jQueryQuestion,QuizResult
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

import uuid
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from .models import QuizInvitation, Candidate

from django.core.mail import send_mail
from .models import QuizInvitation, Candidate
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm, User
import logging
logger = logging.getLogger(__name__)
from .forms import QuizRegistrationForm
from django.urls import reverse



def signIn(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in!")
                return redirect('index')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()
    return render(request, "SignIn.html", {'form': form})

def signUp(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']  # Using email as username
            user.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('index')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = RegisterForm()
    return render(request, "SignUp.html", {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')


def index(request):
    domains = [
        {
            'name': 'java',
            'display_name': 'Java',
            'description': 'How well do you know Java? From object-oriented principles to Java syntax,take this quiz to test your expertise!'
        },
        {
            'name': 'python',
            'display_name': 'Python',
            'description': 'Are you ready to prove your Python skills? Challenge yourself with this quiz and see how you stack up!'
        },
        {
            'name': 'css',
            'display_name': 'CSS',
            'description': 'Ready to test CSS skills? From basic styles to advanced layouts, challenge yourself with this quiz!'
        },
        {
            'name': 'html',
            'display_name': 'HTML',
            'description': 'Know HTML? From basic to advanced structuring, challenge yourself with this quiz and see your rate!'
        },
        {
            'name': 'javascript',
            'display_name': 'JavaScript',
            'description': " From variables to advanced functions, challenge yourself with this quiz and see how well you know JS!"
        },
        {
            'name': 'jquery',
            'display_name': 'jQuery',
            'description': "From DOM manipulation to event handling, Challenge yourself with this quiz and see how well you know jQuery!"
        }
    ]
    
    return render(request, "index.html", {'domains': domains})

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def custom_quiz(request):
    if request.method == 'POST':
        selected_domains = request.POST.getlist('selected_domains')
        return render(request, 'domain_difficulty_selection.html', {
            'selected_domains': selected_domains,
            'difficulty_options': ['mixed', 'easy', 'medium', 'hard']
        })
    return redirect('index')

def generate_quiz(request):
    if not request.user.is_authenticated:
        return redirect('signIn')
        
    if request.method == 'POST':
        domain_difficulties = {}
        for key, value in request.POST.items():
            if key.startswith('difficulty_'):
                domain = key.replace('difficulty_', '')
                domain_difficulties[domain] = value
        
        quiz_id = str(uuid.uuid4())
        invitation = QuizInvitation.objects.create(
            quiz_id=quiz_id,
            created_by=request.user,
            domains=domain_difficulties,
            expiry=timezone.now() + timedelta(days=7)
        )
        
        request.session['current_quiz_id'] = quiz_id
        return redirect('invite_candidates')
    
    return redirect('index')

def invite_candidates(request):
    if not request.user.is_authenticated:
        return redirect('signIn')
        
    quiz_id = request.session.get('current_quiz_id')
    if not quiz_id:
        messages.error(request, "No quiz ID found in session")
        return redirect('index')
    
    try:
        invitation = QuizInvitation.objects.get(quiz_id=quiz_id, created_by=request.user)
    except QuizInvitation.DoesNotExist:
        messages.error(request, "Invalid quiz invitation")
        return redirect('index')
    
    if request.method == 'POST':
        emails = request.POST.get('emails', '').split('\n')
        emails = [email.strip() for email in emails if email.strip()]
        
        if not emails:
            messages.error(request, "Please enter at least one email address")
            return redirect('invite_candidates')
        
        successful_sends = 0
        for email in emails:
            try:
                # First check if candidate already exists
                candidate, created = Candidate.objects.get_or_create(
                    email=email,
                    invitation=invitation,
                    defaults={'token': str(uuid.uuid4())}
                )
                
                if not created:
                    messages.warning(request, f"{email} was already invited")
                    continue
                
                quiz_url = f"{settings.SITE_URL}/quiz/register/{quiz_id}/?token={candidate.token}"
                
                send_mail(
                    f"Invitation to take {', '.join(invitation.domains.keys())} Quiz",
                    f"You've been invited to take a quiz. Click here to participate: {quiz_url}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                successful_sends += 1
                
            except Exception as e:
                logger.error(f"Failed to send to {email}: {str(e)}")
                messages.error(request, f"Failed to send to {email}: {str(e)}")
                continue
        
        # Render the same page with success modal
        return render(request, 'invite_candidates.html', {
            'quiz_id': quiz_id,
            'invitation': invitation,
            'successful_sends': successful_sends,
            'show_success_modal': True
        })
    
    return render(request, 'invite_candidates.html', {
        'quiz_id': quiz_id,
        'invitation': invitation
    })  


@login_required
def take_quiz(request, quiz_id):
    token = request.GET.get('token')
    if not token:
        messages.error(request, "Missing quiz token")
        return redirect('index')
    
    try:
        candidate = Candidate.objects.get(
            token=token,
            invitation__quiz_id=quiz_id,
            user=request.user
        )
        
        if candidate.is_completed:
            # Set a session flag to prevent multiple submissions
            request.session['quiz_completed'] = True
            return render(request, 'quiz_success.html', {'quiz_id': quiz_id})
        
        # Set session timeout to match quiz duration (e.g., 1 hour)
        request.session.set_expiry(3600)
        
        # Store quiz start time
        if 'quiz_start_time' not in request.session:
            request.session['quiz_start_time'] = timezone.now().isoformat()
        
        questions_by_domain = {}
        domain_models = {
            'java': JavaQuestion,
            'python': PythonQuestion,
            'css': CSSQuestion,
            'html': HTMLQuestion,
            'javascript': JavaScriptQuestion,
            'jquery': jQueryQuestion
        }
        
        total_questions = 0
        quiz_title = []
        
        # Clear previous session data
        for domain in candidate.invitation.domains.keys():
            request.session.pop(f'{quiz_id}_{domain}_questions_data', None)
        
        for domain, difficulty in candidate.invitation.domains.items():
            model = domain_models.get(domain.lower())
            if not model:
                continue
                
            qs = model.objects.all()
            if difficulty != 'mixed':
                qs = qs.filter(difficulty=difficulty)
            
            questions = list(qs.order_by('?')[:10])
            questions_by_domain[domain] = questions
            total_questions += len(questions)
            quiz_title.append(domain.capitalize())
            
            # Store complete question data in session
            request.session[f'{quiz_id}_{domain}_questions_data'] = [
                {
                    'id': q.id,
                    'text': q.text,
                    'choices': q.choices,
                    'correct_answer': q.correct_answer
                } for q in questions
            ]
        
        return render(request, 'candidate_quiz.html', {
            'quiz_id': quiz_id,
            'token': token,
            'questions_by_domain': questions_by_domain,
            'total_questions': total_questions,
            'quiz_title': " & ".join(quiz_title)
        })
        
    except Candidate.DoesNotExist:
        messages.error(request, "Invalid quiz access")
        return redirect('index')
    
def quiz_invitations(request):
    invitations = QuizInvitation.objects.filter(created_by=request.user)
    return render(request, 'quiz_invitations.html', {'invitations': invitations})

def quiz_registration(request, quiz_id):
    # Get token from GET or POST
    token = request.GET.get('token') or request.POST.get('token')
    if not token:
        raise Http404("Token is required")

    try:
        # Get candidate record
        candidate = Candidate.objects.get(token=token, invitation__quiz_id=quiz_id)
        candidate_email = candidate.email.lower().strip()  # Normalized email
    except Candidate.DoesNotExist:
        raise Http404("No candidate found with this token")

    # Determine if we should show login tab
    show_login = 'show_login' in request.GET or (
        request.method == 'POST' and request.POST.get('form_type') == 'login'
    )

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'login':
            # Handle login attempt
            email = request.POST.get('email', '').lower().strip()  # Normalized
            password = request.POST.get('password', '').strip()
            
            # Authenticate user
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                # Verify email matches candidate email
                if user.email.lower().strip() == candidate_email:
                    # Link user to candidate if not already linked
                    if candidate.user != user:
                        candidate.user = user
                        candidate.save()
                    
                    login(request, user)
                    # Redirect to instructions with token
                    return redirect(f'/quiz-instructions/{quiz_id}/?token={token}')
                else:
                    messages.error(request, "This email doesn't match the invitation")
            else:
                messages.error(request, "Invalid email or password")
            
            # Stay on login tab if login fails
            show_login = True
            
        else:
            # Handle registration attempt
            form = QuizRegistrationForm(request.POST)
            if form.is_valid():
                try:
                    # Create new user
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=candidate_email,  # Use normalized email
                        password=form.cleaned_data['password1']
                    )
                    # Link user to candidate
                    candidate.user = user
                    candidate.save()
                    # Log user in
                    login(request, user)
                    # Redirect to instructions
                    return redirect(f'/quiz-instructions/{quiz_id}/?token={token}')
                except Exception as e:
                    messages.error(request, f"Registration failed: {str(e)}")
            else:
                # Show form errors
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
    
    # Initialize form for GET requests or failed POSTs
    form = QuizRegistrationForm(initial={'email': candidate_email}) if not show_login else None
    
    return render(request, 'quiz_registration.html', {
        'form': form,
        'quiz_id': quiz_id,
        'token': token,
        'candidate_email': candidate_email,
        'show_login': show_login
    })

@login_required
def quiz_instructions(request, quiz_id):
    token = request.GET.get('token')
    if not token:
        messages.error(request, "Missing quiz token")
        return redirect('index')
    
    print(f"Debug: Instructions - Quiz ID: {quiz_id}, Token: {token}")  # Debug
    
    try:
        candidate = Candidate.objects.get(
            invitation__quiz_id=quiz_id,
            user=request.user,
            token=token
        )
        return render(request, 'quiz_instructions.html', {
            'quiz_id': quiz_id,
            'token': token
        })
    except Candidate.DoesNotExist:
        messages.error(request, "Invalid quiz access")
        return redirect('index')



def view_sent_invites(request):
    quiz_id = request.GET.get('quiz_id')
    if not quiz_id:
        return redirect('index')
    
    invitation = QuizInvitation.objects.get(quiz_id=quiz_id)
    candidates = Candidate.objects.filter(invitation=invitation)
    
    return render(request, 'sent_invites.html', {
        'quiz_id': quiz_id,
        'candidates': candidates,
        'invitation': invitation
    })



@login_required
def submit_quiz(request, quiz_id):
    token = request.GET.get('token') or request.POST.get('token')
    if not token:
        messages.error(request, "Missing quiz token")
        return redirect('index')

    try:
        candidate = Candidate.objects.get(
            token=token,
            invitation__quiz_id=quiz_id,
            user=request.user
        )
        
        if candidate.is_completed:
            return redirect('quiz_success', quiz_id=quiz_id)
        
        # Get answers from either POST data or saved progress
        if request.method == 'POST':
            answers = dict(request.POST)
        else:
            progress = request.session.get('quiz_progress', {})
            if str(progress.get('quiz_id')) == str(quiz_id) and progress.get('token') == str(token):
                answers = progress.get('answers', {})
            else:
                answers = {}
        
        # Calculate summary statistics
        summary = {}
        for domain in candidate.invitation.domains.keys():
            questions_data = request.session.get(f'{quiz_id}_{domain}_questions_data', [])
            answered = 0
            
            for question in questions_data:
                if answers.get(f'question_{question["id"]}'):
                    answered += 1
            
            summary[domain] = {
                'total': len(questions_data),
                'answered': answered,
                'unanswered': len(questions_data) - answered
            }
        
        # Store in session for final submission
        request.session['quiz_answers'] = {
            'quiz_id': str(quiz_id),
            'token': str(token),
            'answers': answers,
            'summary': summary
        }
        
        return render(request, 'quiz_submission.html', {
            'quiz_id': quiz_id,
            'token': token,
            'summary': summary
        })
        
    except Candidate.DoesNotExist:
        messages.error(request, "Invalid quiz submission")
        return redirect('index')
    

@csrf_exempt
def save_progress(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quiz_id = data.get('quiz_id')
            token = data.get('token')
            
            if not quiz_id or not token:
                return JsonResponse({'status': 'error', 'message': 'Missing parameters'}, status=400)
            
            # Store answers in session
            request.session['quiz_progress'] = {
                'quiz_id': str(quiz_id),
                'token': str(token),
                'answers': data.get('answers', {})
            }
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

@login_required
def final_submit(request, quiz_id):
    token = request.GET.get('token')
    if not token:
        messages.error(request, "Missing quiz token")
        return redirect('index')

    try:
        candidate = Candidate.objects.get(
            token=token,
            invitation__quiz_id=quiz_id,
            user=request.user
        )
        
        if candidate.is_completed:
            return redirect('quiz_success', quiz_id=quiz_id)
        
        # Get answers from session
        quiz_data = request.session.get('quiz_answers', {})
        if not quiz_data or str(quiz_data.get('quiz_id')) != str(quiz_id):
            messages.error(request, "Session expired. Please retake the quiz.")
            return redirect('take_quiz', quiz_id=quiz_id)
        
        # Calculate scores
        domain_scores = {}
        total_correct = 0
        total_questions = 0
        
        for domain in candidate.invitation.domains.keys():
            questions_data = request.session.get(f'{quiz_id}_{domain}_questions_data', [])
            correct = 0
            
            for question in questions_data:
                total_questions += 1
                user_answer = quiz_data['answers'].get(f'question_{question["id"]}')
                
                if user_answer and user_answer[0].lower() == question['correct_answer'].lower():
                    correct += 1
            
            domain_scores[domain] = {
                'correct': correct,
                'total': len(questions_data),
                'percentage': round((correct / len(questions_data)) * 100, 2) if len(questions_data) > 0 else 0
            }
            total_correct += correct
        
        percentage = round((total_correct / total_questions) * 100, 2) if total_questions > 0 else 0
        
        # Save results
        QuizResult.objects.create(
            candidate=candidate,
            quiz=candidate.invitation,
            domain_scores=domain_scores,
            total_score=total_correct,
            percentage=percentage,
            submitted_at=timezone.now()
        )
        
        # Mark candidate as completed
        candidate.is_completed = True
        candidate.completed_at = timezone.now()
        candidate.save()
        
        # Clear session data
        for domain in candidate.invitation.domains.keys():
            request.session.pop(f'{quiz_id}_{domain}_questions_data', None)
        request.session.pop('quiz_answers', None)
        request.session.pop('quiz_progress', None)
        
        return redirect(reverse('quiz_success', kwargs={'quiz_id': quiz_id}) + f'?token={token}')
        
    except Candidate.DoesNotExist:
        messages.error(request, "Invalid quiz submission")
        return redirect('index')
    

@login_required
def quiz_success(request, quiz_id):
    token = request.GET.get('token')
    if not token:
        return render(request, 'quiz_success.html', {'quiz_id': quiz_id})
    
    try:
        candidate = Candidate.objects.get(
            token=token,
            invitation__quiz_id=quiz_id,
            user=request.user
        )
        return render(request, 'quiz_success.html', {'quiz_id': quiz_id})
    except Candidate.DoesNotExist:
        return render(request, 'quiz_success.html', {'quiz_id': quiz_id})