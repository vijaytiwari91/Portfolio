import time
from django.db import transaction, connections
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from .models import (
    AboutSection, Skill, Project, Experience, 
    Education, ContactMessage
)
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


from .forms import (
    AboutSectionForm, SkillForm, ProjectForm, 
    ExperienceForm, EducationForm, ContactForm
)

def home(request):
    """Homepage view with portfolio overview"""
    try:
        about = AboutSection.objects.first()
    except AboutSection.DoesNotExist:
        about = None
    
    featured_projects = Project.objects.filter(is_featured=True, is_published=True)[:6]
    featured_skills = Skill.objects.filter(is_featured=True)[:8]
    recent_experience = Experience.objects.all()[:3]
    
    context = {
        'about': about,
        'featured_projects': featured_projects,
        'featured_skills': featured_skills,
        'recent_experience': recent_experience,
    }
    return render(request, 'portfolio/home.html', context)

# Your view function
def projects(request):
    """
    Display all published portfolio projects.
    
    This view:
    1. Fetches only published projects from the database
    2. Orders them by the 'order' field, then by creation date (newest first)
    3. Passes the data to the template
    """
    
    # Get only published projects, ordered by custom order then by creation date
    portfolio_projects = Project.objects.filter(
        is_published=True
    ).order_by('order', '-created_at')
    
    # You can also add filtering for featured projects if needed
    featured_projects = portfolio_projects.filter(is_featured=True)
    
    # Get unique project types for any filtering you might want to add later
    project_types = Project.objects.filter(
        is_published=True
    ).values_list('project_type', flat=True).distinct()
    
    context = {
        'projects': portfolio_projects,
        'featured_projects': featured_projects,
        'project_types': project_types,
        # Note: all_technologies removed since your table doesn't have this relationship
        # You'll need to create a separate technology table if you want this feature
    }
    
    return render(request, 'portfolio/projects.html', context)

def project_detail(request, slug):
    """Individual project detail page"""
    project = get_object_or_404(Project, slug=slug, is_published=True)
    related_projects = Project.objects.filter(
        is_published=True, 
        project_type=project.project_type
    ).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'portfolio/project_detail.html', context)

def experience(request):
    """Experience page view"""
    experiences = Experience.objects.all().order_by('-is_current', 'order')
    education = Education.objects.all().order_by('order')
    
    # Add skill categories for the Skills section
    skill_categories = {
        'programming': Skill.objects.filter(category='programming').order_by('order'),
        'frontend': Skill.objects.filter(category='frontend').order_by('order'),
        'backend': Skill.objects.filter(category='backend').order_by('order'),
        'database': Skill.objects.filter(category='database').order_by('order'),
        'devops': Skill.objects.filter(category='devops').order_by('order'),
        'other': Skill.objects.filter(category='other').order_by('order'),
    }
    
    try:
        about = AboutSection.objects.first()
    except AboutSection.DoesNotExist:
        about = None
    
    # Debug info
    print("Experiences count:", experiences.count())
    print("Education count:", education.count())
    print("Skills count:", sum(len(skills) for skills in skill_categories.values()))
    
    context = {
        'experiences': experiences,
        'education': education,
        'skill_categories': skill_categories,
        'about': about,
        'debug': True,  # Enable debug mode in template
    }
    return render(request, 'portfolio/experience.html', context)

def contact(request):
    """Contact page with form"""
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            try:

                name = form.cleaned_data['name']
                email = form.cleaned_data['email']
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

                print("Sending email with subject:", subject)
                print("Full message content:", full_message)
                send_mail(
                subject=subject,
                message=full_message,
                from_email=email,  # or DEFAULT_FROM_EMAIL
                recipient_list=['gvedhanth123@gmail.com'],  # Where you receive emails
                fail_silently=False,
                )

                # Use a transaction with a timeout to prevent database locks
                with transaction.atomic():
                    contact_msg = form.save(commit=False)
                    contact_msg.save()
                    
                    # Close database connections to release locks
                    for conn in connections.all():
                        conn.close()
                        
                    messages.success(request, 'Thank you! Your message has been sent successfully.')
                    return redirect('portfolio:contact')
                
            except Exception as e:
                # If there's a database error, show an error message
                print(e)
                messages.error(request, f'Sorry, we could not send your message. Please try again later.')
    else:
        form = ContactForm()
    
    try:
        about = AboutSection.objects.first()
    except AboutSection.DoesNotExist:
        about = None
    
    # Add hardcoded FAQs until a model is created
    faqs = [
        {
            'question': 'What services do you offer?',
            'answer': 'I specialize in full-stack web development, data analysis, and machine learning solutions. My services include custom web application development, data visualization, predictive modeling, and technical consulting.'
        },
        {
            'question': 'How much do your services cost?',
            'answer': 'Project costs vary based on complexity, timeline, and specific requirements. I offer competitive rates and would be happy to provide a detailed quote after discussing your project needs.'
        },        
        {
            'question': 'What is your typical project timeline?',
            'answer': 'Timeline depends on project scope and complexity. Small websites typically take 2-4 weeks, while complex web applications may take 2-6 months. I\'ll provide a detailed timeline during our initial consultation.'
        },
        {
            'question': 'Do you offer ongoing maintenance and support?',
            'answer': 'Yes, I offer maintenance packages and ongoing support for all completed projects. This ensures your application remains secure, up-to-date, and functioning optimally.'
        },
    ]
    
    context = {
        'form': form,
        'about': about,
        'faqs': faqs,
    }
    return render(request, 'portfolio/contact.html', context)

# Admin/Dashboard Views
@staff_member_required   # <-- Only admin/staff can access
@login_required           # <-- Must be logged in
def dashboard(request):
    """Admin dashboard view"""
    stats = {
        'projects': Project.objects.count(),
        'published_projects': Project.objects.filter(is_published=True).count(),
        'skills': Skill.objects.count(),
        'experiences': Experience.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'total_messages': ContactMessage.objects.count(),
    }
    
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
    recent_projects = Project.objects.order_by('-created_at')[:5]
    
    context = {
        'stats': stats,
        'recent_messages': recent_messages,
        'recent_projects': recent_projects,
    }
    return render(request, 'portfolio/dashboard.html', context)

@login_required           # <-- Must be logged in
@staff_member_required
def edit_about(request):
    """Edit about section"""
    try:
        about = AboutSection.objects.first()
    except AboutSection.DoesNotExist:
        about = None
    
    if request.method == 'POST':
        form = AboutSectionForm(request.POST, request.FILES, instance=about)
        if form.is_valid():
            form.save()
            messages.success(request, 'About section updated successfully!')
            return redirect('portfolio:dashboard')
    else:
        form = AboutSectionForm(instance=about)
    
    context = {
        'form': form,
        'about': about,
    }
    return render(request, 'portfolio/edit_about.html', context)

@login_required           # <-- Must be logged in
@staff_member_required
def manage_projects(request):
    """Manage projects view"""
    projects = Project.objects.all().order_by('-created_at')
    
    context = {
        'projects': projects,
    }
    return render(request, 'portfolio/manage_projects.html', context)
@login_required           # <-- Must be logged in
@staff_member_required
def edit_project(request, project_id=None):
    """Add/Edit project"""
    if project_id:
        project = get_object_or_404(Project, id=project_id)
    else:
        project = None
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f'Project {"updated" if project else "created"} successfully!')
            return redirect('portfolio:manage_projects')
    else:
        form = ProjectForm(instance=project)
    
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'portfolio/edit_project.html', context)

@login_required           # <-- Must be logged in
@staff_member_required
def manage_skills(request):
    """Manage skills view"""
    skills = Skill.objects.all().order_by('category', 'order')
    
    context = {
        'skills': skills,
    }
    return render(request, 'portfolio/manage_skills.html', context)

@login_required           # <-- Must be logged in
@staff_member_required
def edit_skill(request, skill_id=None):
    """Add/Edit skill"""
    if skill_id:
        skill = get_object_or_404(Skill, id=skill_id)
    else:
        skill = None
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, f'Skill {"updated" if skill else "created"} successfully!')
            return redirect('portfolio:manage_skills')
    else:
        form = SkillForm(instance=skill)
    
    context = {
        'form': form,
        'skill': skill,
    }
    return render(request, 'portfolio/edit_skill.html', context)

@login_required           # <-- Must be logged in
@staff_member_required
def manage_messages(request):
    """Manage contact messages"""
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    
    # Pagination
    paginator = Paginator(messages_list, 20)
    page_number = request.GET.get('page')
    messages_page = paginator.get_page(page_number)
    
    context = {
        'messages': messages_page,
    }
    return render(request, 'portfolio/manage_messages.html', context)

@login_required           # <-- Must be logged in
@staff_member_required
def mark_message_read(request, message_id):
    """Mark message as read/unread"""
    if request.method == 'POST':
        message = get_object_or_404(ContactMessage, id=message_id)
        message.is_read = not message.is_read
        message.save()
        
        status = 'read' if message.is_read else 'unread'
        messages.success(request, f'Message marked as {status}.')
    
    return redirect('portfolio:manage_messages')

# API Views for AJAX
@login_required           # <-- Must be logged in
@staff_member_required
def delete_project(request, project_id):
    """Delete project via AJAX"""
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required           # <-- Must be logged in
@staff_member_required
def delete_skill(request, skill_id):
    """Delete skill via AJAX"""
    if request.method == 'POST':
        skill = get_object_or_404(Skill, id=skill_id)
        skill.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# Create your views here.
