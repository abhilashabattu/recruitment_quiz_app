from django.contrib import admin

# Register your models here.
from .models import User, JavaQuestion, CSSQuestion, HTMLQuestion, PythonQuestion, JavaScriptQuestion, jQueryQuestion,QuizResult
from .models import QuizInvitation, Candidate
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

# Register the User model with the custom admin class
admin.site.register(User, CustomUserAdmin)

class CandidateInline(admin.TabularInline):
    model = Candidate
    extra = 0
    readonly_fields = ('token', 'is_completed', 'created_at')
    fields = ('email', 'token', 'is_completed', 'created_at')

@admin.register(QuizInvitation)
class QuizInvitationAdmin(admin.ModelAdmin):
    list_display = ('quiz_id', 'created_by', 'created_at', 'expiry')
    list_filter = ('created_at', 'expiry')
    search_fields = ('quiz_id', 'created_by__username')
    inlines = [CandidateInline]
    readonly_fields = ('quiz_id', 'created_by', 'created_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('email', 'invitation', 'is_completed', 'created_at', 'completed_at')
    list_filter = ('is_completed', 'created_at', 'completed_at')
    search_fields = ('email', 'invitation__quiz_id')
    readonly_fields = ('token', 'created_at', 'completed_at')
    fieldsets = (
        (None, {
            'fields': ('email', 'invitation', 'user', 'token')
        }),
        ('Status', {
            'fields': ('is_completed', 'created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(invitation__created_by=request.user)
    
    
@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'quiz', 'total_score', 'percentage', 'submitted_at')
    list_filter = ('submitted_at', 'quiz__created_by')
    search_fields = ('candidate__email', 'quiz__quiz_id')
    readonly_fields = ('submitted_at',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(quiz__created_by=request.user)
    
    fieldsets = (
        (None, {
            'fields': ('candidate', 'quiz', 'submitted_at')
        }),
        ('Scores', {
            'fields': ('domain_scores', 'total_score', 'percentage'),
            'classes': ('collapse',)
        }),
    )

    def domain_scores_display(self, obj):
        return ", ".join([f"{k}: {v['correct']}/{v['total']}" for k, v in obj.domain_scores.items()])
    domain_scores_display.short_description = 'Domain Scores'


@admin.register(JavaQuestion)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'difficulty', 'question_type')
    list_filter = ('difficulty', 'question_type')
    search_fields = ('text',)


@admin.register(CSSQuestion)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'difficulty', 'question_type')
    list_filter = ('difficulty', 'question_type')
    search_fields = ('text',)

@admin.register(HTMLQuestion)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'difficulty', 'question_type')
    list_filter = ('difficulty', 'question_type')
    search_fields = ('text',)

@admin.register(PythonQuestion)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'difficulty', 'question_type')
    list_filter = ('difficulty', 'question_type')
    search_fields = ('text',)

@admin.register(JavaScriptQuestion)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'difficulty', 'question_type')
    list_filter = ('difficulty', 'question_type')
    search_fields = ('text',)

@admin.register(jQueryQuestion)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'difficulty', 'question_type')
    list_filter = ('difficulty', 'question_type')
    search_fields = ('text',)
