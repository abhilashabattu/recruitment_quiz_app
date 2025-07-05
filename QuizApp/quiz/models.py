from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class QuizInvitation(models.Model):
    quiz_id = models.CharField(max_length=36, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    domains = models.JSONField()  # Stores {'domain': 'difficulty'} pairs
    created_at = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()

    @property
    def completed_count(self):
        return self.candidate_set.filter(is_completed=True).count()

class Candidate(models.Model):
    email = models.EmailField()
    invitation = models.ForeignKey(QuizInvitation, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Add this field

    def __str__(self):
        return f"{self.email} - {self.invitation.quiz_id}"


class QuizResult(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    quiz = models.ForeignKey(QuizInvitation, on_delete=models.CASCADE)
    domain_scores = models.JSONField()  # {'domain': {'correct': X, 'total': Y}}
    total_score = models.IntegerField()
    percentage = models.FloatField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.candidate.email} - {self.quiz.quiz_id} - {self.percentage}%" 



class JavaQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    QUESTION_TYPE_CHOICES = [
        ('obj', 'Objective'),
        ('sub', 'Subjective'),
    ]

    text = models.TextField()
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    question_type = models.CharField(
        max_length=3, 
        choices=QUESTION_TYPE_CHOICES, 
        default='obj' 
    )
    choices = models.JSONField(  #  multiple-choice options
        help_text="Enter choices as a list (e.g., ['Option A', 'Option B'])",
        default=list
    )
    correct_answer = models.CharField(
        max_length=2,
        help_text="Correct answer key (e.g., 'a', 'b', etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]} ({self.difficulty})"



class CSSQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    QUESTION_TYPE_CHOICES = [
        ('obj', 'Objective'),
        ('sub', 'Subjective'),
    ]

    text = models.TextField()
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    question_type = models.CharField(
        max_length=3, 
        choices=QUESTION_TYPE_CHOICES, 
        default='obj' 
    )
    choices = models.JSONField(  #  multiple-choice options
        help_text="Enter choices as a list (e.g., ['Option A', 'Option B'])",
        default=list
    )
    correct_answer = models.CharField(
        max_length=2,
        help_text="Correct answer key (e.g., 'a', 'b', etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]} ({self.difficulty})"

class HTMLQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    QUESTION_TYPE_CHOICES = [
        ('obj', 'Objective'),
        ('sub', 'Subjective'),
    ]

    text = models.TextField()
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    question_type = models.CharField(
        max_length=3, 
        choices=QUESTION_TYPE_CHOICES, 
        default='obj' 
    )
    choices = models.JSONField(  #  multiple-choice options
        help_text="Enter choices as a list (e.g., ['Option A', 'Option B'])",
        default=list
    )
    correct_answer = models.CharField(
        max_length=2,
        help_text="Correct answer key (e.g., 'a', 'b', etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]} ({self.difficulty})"

class PythonQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    QUESTION_TYPE_CHOICES = [
        ('obj', 'Objective'),
        ('sub', 'Subjective'),
    ]

    text = models.TextField()
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    question_type = models.CharField(
        max_length=3, 
        choices=QUESTION_TYPE_CHOICES, 
        default='obj' 
    )
    choices = models.JSONField(  #  multiple-choice options
        help_text="Enter choices as a list (e.g., ['Option A', 'Option B'])",
        default=list
    )
    correct_answer = models.CharField(
        max_length=2,
        help_text="Correct answer key (e.g., 'a', 'b', etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]} ({self.difficulty})"


class JavaScriptQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    QUESTION_TYPE_CHOICES = [
        ('obj', 'Objective'),
        ('sub', 'Subjective'),
    ]

    text = models.TextField()
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    question_type = models.CharField(
        max_length=3, 
        choices=QUESTION_TYPE_CHOICES, 
        default='obj' 
    )
    choices = models.JSONField(  #  multiple-choice options
        help_text="Enter choices as a list (e.g., ['Option A', 'Option B'])",
        default=list
    )
    correct_answer = models.CharField(
        max_length=2,
        help_text="Correct answer key (e.g., 'a', 'b', etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]} ({self.difficulty})"


class jQueryQuestion(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    QUESTION_TYPE_CHOICES = [
        ('obj', 'Objective'),
        ('sub', 'Subjective'),
    ]

    text = models.TextField()
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY_CHOICES)
    question_type = models.CharField(
        max_length=3, 
        choices=QUESTION_TYPE_CHOICES, 
        default='obj' 
    )
    choices = models.JSONField(  #  multiple-choice options
        help_text="Enter choices as a list (e.g., ['Option A', 'Option B'])",
        default=list
    )
    correct_answer = models.CharField(
        max_length=2,
        help_text="Correct answer key (e.g., 'a', 'b', etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text[:50]} ({self.difficulty})"

