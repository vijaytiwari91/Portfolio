from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Public views
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('experience/', views.experience, name='experience'),
    path('contact/', views.contact, name='contact'),
    
    # Admin/Dashboard views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/about/edit/', views.edit_about, name='edit_about'),
    
    # Project management
    path('dashboard/projects/', views.manage_projects, name='manage_projects'),
    path('dashboard/projects/add/', views.edit_project, name='add_project'),
    path('dashboard/projects/edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('dashboard/projects/delete/<int:project_id>/', views.delete_project, name='delete_project'),
    
    # Skill management
    path('dashboard/skills/', views.manage_skills, name='manage_skills'),
    path('dashboard/skills/add/', views.edit_skill, name='add_skill'),
    path('dashboard/skills/edit/<int:skill_id>/', views.edit_skill, name='edit_skill'),
    path('dashboard/skills/delete/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    
    # Message management
    path('dashboard/messages/', views.manage_messages, name='manage_messages'),
    path('dashboard/messages/mark-read/<int:message_id>/', views.mark_message_read, name='mark_message_read'),
]
