from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import AboutSection, Skill, Project, Experience, Education, ContactMessage
from .forms import *
from .decorators import admin_required

@admin_required
def dashboard_home(request):
    """Main dashboard view with overview of all content"""
    context = {
        'about_section': AboutSection.objects.first(),
        'total_projects': Project.objects.count(),
        'featured_projects': Project.objects.filter(is_featured=True).count(),
        'total_skills': Skill.objects.count(),
        'featured_skills': Skill.objects.filter(is_featured=True).count(),
        'total_experience': Experience.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'recent_projects': Project.objects.filter(is_published=True)[:3],
        'recent_messages': ContactMessage.objects.filter(is_read=False)[:5],
    }
    return render(request, 'admin/dashboard/home_simple.html', context)

@admin_required
def quick_edit_about(request):
    """Quick edit form for about section"""
    about, created = AboutSection.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        form = QuickAboutForm(request.POST, request.FILES, instance=about)
        if form.is_valid():
            form.save()
            messages.success(request, 'About section updated successfully!')
            return redirect('portfolio:dashboard_home')
    else:
        form = QuickAboutForm(instance=about)
    
    return render(request, 'admin/dashboard/quick_edit_about.html', {
        'form': form,
        'about': about    })

@admin_required
def manage_projects(request):
    """Project management interface"""
    projects = Project.objects.all().order_by('-is_featured', 'order', '-created_at')
    return render(request, 'admin/dashboard/manage_projects.html', {
        'projects': projects    })

@admin_required
def manage_skills(request):
    """Skills management interface"""
    skills = Skill.objects.all().order_by('category', 'order', 'name')
    return render(request, 'admin/dashboard/manage_skills.html', {
        'skills': skills    })

@admin_required
@require_POST
def toggle_project_featured(request, project_id):
    """Ajax endpoint to toggle project featured status"""
    project = get_object_or_404(Project, id=project_id)
    project.is_featured = not project.is_featured
    project.save()
    
    return JsonResponse({
        'success': True,
        'is_featured': project.is_featured,
        'message': f'Project {"featured" if project.is_featured else "unfeatured"} successfully!'    })

@admin_required
@require_POST
def toggle_skill_featured(request, skill_id):
    """Ajax endpoint to toggle skill featured status"""
    skill = get_object_or_404(Skill, id=skill_id)
    skill.is_featured = not skill.is_featured
    skill.save()
    
    return JsonResponse({
        'success': True,
        'is_featured': skill.is_featured,
        'message': f'Skill {"featured" if skill.is_featured else "unfeatured"} successfully!'    })

@admin_required
@require_POST
def mark_message_read(request, message_id):
    """Mark contact message as read"""
    message = get_object_or_404(ContactMessage, id=message_id)
    message.is_read = True
    message.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Message marked as read!'
    })

def dashboard_debug(request):
    """Simple debug view to test template rendering"""
    context = {
        'debug_message': 'Template rendering is working!',
        'total_projects': Project.objects.count(),
    }
    return render(request, 'admin/dashboard/minimal.html', context)
