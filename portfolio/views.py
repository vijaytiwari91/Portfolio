from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import (
    AboutSection, Skill, Project, Experience, 
    Education, ContactMessage
)
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

def about(request):
    """About page view"""
    try:
        about_section = AboutSection.objects.first()
    except AboutSection.DoesNotExist:
        about_section = None
    
    skills_by_category = {}
    for skill in Skill.objects.all():
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    education = Education.objects.all()
    
    context = {
        'about_section': about_section,
        'skills_by_category': skills_by_category,
        'education': education,
    }
    return render(request, 'portfolio/about.html', context)

def projects(request):
    """Projects listing page"""
    project_list = Project.objects.filter(is_published=True)
    
    # Filter by project type
    project_type = request.GET.get('type')
    if project_type:
        project_list = project_list.filter(project_type=project_type)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        project_list = project_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(project_list, 9)  # 9 projects per page
    page_number = request.GET.get('page')
    projects_page = paginator.get_page(page_number)
    
    # Get project types for filter
    project_types = Project.PROJECT_TYPES
    
    context = {
        'projects': projects_page,
        'project_types': project_types,
        'current_type': project_type,
        'search_query': search_query,
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
    experiences = Experience.objects.all()
    education = Education.objects.all()
    
    context = {
        'experiences': experiences,
        'education': education,
    }
    return render(request, 'portfolio/experience.html', context)

def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent successfully.')
            return redirect('portfolio:contact')
    else:
        form = ContactForm()
    
    try:
        about = AboutSection.objects.first()
    except AboutSection.DoesNotExist:
        about = None
    
    context = {
        'form': form,
        'about': about,
    }
    return render(request, 'portfolio/contact.html', context)

# Admin/Dashboard Views
@staff_member_required
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

@staff_member_required
def manage_projects(request):
    """Manage projects view"""
    projects = Project.objects.all().order_by('-created_at')
    
    context = {
        'projects': projects,
    }
    return render(request, 'portfolio/manage_projects.html', context)

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

@staff_member_required
def manage_skills(request):
    """Manage skills view"""
    skills = Skill.objects.all().order_by('category', 'order')
    
    context = {
        'skills': skills,
    }
    return render(request, 'portfolio/manage_skills.html', context)

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
@staff_member_required
def delete_project(request, project_id):
    """Delete project via AJAX"""
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@staff_member_required
def delete_skill(request, skill_id):
    """Delete skill via AJAX"""
    if request.method == 'POST':
        skill = get_object_or_404(Skill, id=skill_id)
        skill.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# Create your views here.
