from django import forms
from django.forms import ModelForm
from .models import (
    AboutSection, Skill, Project, Experience, 
    Education, ContactMessage
)

class AboutSectionForm(ModelForm):
    """Form for editing About section"""
    class Meta:
        model = AboutSection
        fields = [
            'title', 'description', 'profile_image', 'resume_file',
            'email', 'phone', 'location', 'linkedin_url', 
            'github_url', 'website_url'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
            'website_url': forms.URLInput(attrs={'class': 'form-control'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'resume_file': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class SkillForm(ModelForm):
    """Form for adding/editing skills"""
    class Meta:
        model = Skill
        fields = [
            'name', 'category', 'icon', 'is_featured', 'order'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'e.g., fas fa-code, fab fa-python'
            }),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProjectForm(ModelForm):
    """Form for adding/editing projects"""
    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'short_description', 'description', 
            'project_type', 'technologies', 'image', 'live_url', 
            'github_url', 'demo_url', 'is_featured', 'is_published', 'order'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'short_description': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
            'project_type': forms.Select(attrs={'class': 'form-control'}),
            'technologies': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 8}),
            'live_url': forms.URLInput(attrs={'class': 'form-control'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control'}),
            'demo_url': forms.URLInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ExperienceForm(ModelForm):
    """Form for adding/editing experience"""
    class Meta:
        model = Experience
        fields = [
            'company_name', 'position', 'experience_type', 'description',
            'technologies_used', 'start_date', 'end_date', 'company_url',
            'location', 'is_current', 'order'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'technologies_used': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 6}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'company_url': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class EducationForm(ModelForm):
    """Form for adding/editing education"""
    class Meta:
        model = Education
        fields = [
            'institution_name', 'degree', 'degree_type', 'field_of_study',
            'description', 'gpa', 'start_date', 'end_date', 'institution_url',
            'location', 'is_current', 'order'
        ]
        widgets = {
            'institution_name': forms.TextInput(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'degree_type': forms.Select(attrs={'class': 'form-control'}),
            'field_of_study': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'gpa': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'institution_url': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ContactForm(ModelForm):
    """Contact form for visitors"""
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Your Message'
            }),
        }

class QuickContactForm(forms.Form):
    """Quick contact form for modals"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your Email'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Your Message'
        })
    )
