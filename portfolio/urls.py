from django.urls import path
from . import views
from . import dashboard_views
from . import auth_views

app_name = 'portfolio'

urlpatterns = [    # Public views
    path('', views.home, name='home'),
    path('projects/', views.projects, name='projects'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('experience/', views.experience, name='experience'),
    path('contact/', views.contact, name='contact'),
      # Authentication views
    path('admin/login/', auth_views.admin_login_view, name='admin_login'),
    path('auth/login/', auth_views.admin_login_view, name='auth_login'),  # Django LOGIN_URL
    path('admin/logout/', auth_views.admin_logout_view, name='admin_logout'),
    path('admin/password-reset/', auth_views.password_reset_request, name='password_reset_request'),
    path('admin/password-reset/verify/', auth_views.password_reset_verify, name='password_reset_verify'),
    path('admin/profile/', auth_views.admin_profile, name='admin_profile'),
    path('admin/check-session/', auth_views.check_session_status, name='check_session_status'),
    
    # Debug authentication view (temporary)
    path('admin/login/debug/', auth_views.admin_login_debug_view, name='admin_login_debug'),

    # Debug dashboard view (temporary)
    path('dashboard/debug/', dashboard_views.dashboard_debug, name='dashboard_debug'),

    # Dashboard views (secured with staff_member_required)
    path('dashboard/', dashboard_views.dashboard_home, name='dashboard_home'),
    path('dashboard/about/edit/', dashboard_views.quick_edit_about, name='quick_edit_about'),
    path('dashboard/projects/', dashboard_views.manage_projects, name='manage_projects'),
    path('dashboard/skills/', dashboard_views.manage_skills, name='manage_skills'),
    
    # Ajax endpoints (secured with staff_member_required)
    path('dashboard/project/<int:project_id>/toggle-featured/', dashboard_views.toggle_project_featured, name='toggle_project_featured'),
    path('dashboard/skill/<int:skill_id>/toggle-featured/', dashboard_views.toggle_skill_featured, name='toggle_skill_featured'),
    path('dashboard/message/<int:message_id>/mark-read/', dashboard_views.mark_message_read, name='mark_message_read'),
]
