from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    AboutSection, Skill, Project, Experience, 
    Education, ContactMessage
)

@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'email', 'location', 'profile_image_preview', 'updated_at']
    search_fields = ['title', 'description', 'email']
    readonly_fields = ['created_at', 'updated_at', 'profile_image_preview']
    
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.profile_image.url
            )
        return "No image"
    profile_image_preview.short_description = 'Profile Image'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'profile_image', 'profile_image_preview')
        }),        ('Contact Information', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Social Links', {
            'fields': ('linkedin_url', 'github_url', 'website_url')
        }),
        ('Documents', {
            'fields': ('resume_file',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_featured', 'order']
    list_filter = ['category', 'is_featured']
    search_fields = ['name']
    list_editable = ['order', 'is_featured']
    ordering = ['category', 'order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'category')
        }),
        ('Display Options', {
            'fields': ('icon', 'is_featured', 'order')
        }),
    )

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'project_type', 'image_preview', 'is_featured', 'is_published', 'order', 'created_at']
    list_filter = ['project_type', 'is_featured', 'is_published', 'created_at']
    search_fields = ['title', 'description', 'short_description']
    list_editable = ['is_featured', 'is_published', 'order']v
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    ordering = ['-is_featured', 'order', '-created_at']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'project_type', 'short_description', 'description')
        }),
        ('Media & Links', {
            'fields': ('image', 'live_url', 'github_url', 'demo_url')
        }),
        ('Technologies', {
            'fields': ('technologies',)
        }),
        ('Display Options', {
            'fields': ('is_featured', 'is_published', 'order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

    def get_technologies(self, obj):
        return ", ".join([skill.name for skill in obj.technologies.all()[:3]])
    get_technologies.short_description = 'Technologies'

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['position', 'company_name', 'experience_type', 'start_date', 'end_date', 'is_current', 'order']
    list_filter = ['experience_type', 'is_current', 'start_date']
    search_fields = ['position', 'company_name', 'description']
    list_editable = ['is_current', 'order']
    filter_horizontal = ['technologies_used']
    ordering = ['-start_date', 'order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('company_name', 'position', 'experience_type', 'description')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Additional Information', {
            'fields': ('company_url', 'location', 'technologies_used')
        }),
        ('Display Options', {
            'fields': ('order',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.is_current:
            obj.end_date = None
        super().save_model(request, obj, form, change)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution_name', 'degree_type', 'start_date', 'end_date', 'is_current', 'order']
    list_filter = ['degree_type', 'is_current', 'start_date']
    search_fields = ['degree', 'institution_name', 'field_of_study']
    list_editable = ['is_current', 'order']
    ordering = ['-start_date', 'order']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('institution_name', 'degree', 'degree_type', 'field_of_study', 'description')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Additional Information', {
            'fields': ('gpa', 'institution_url', 'location')
        }),
        ('Display Options', {
            'fields': ('order',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.is_current:
            obj.end_date = None
        super().save_model(request, obj, form, change)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    list_editable = ['is_read']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        return False
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields
        else:
            return []

# Custom admin site header - using a function to get the name from the database
def update_admin_headers():
    try:
        # Try to get the About section from the database
        about = AboutSection.objects.first()
        if about:
            # If about section exists, use the title from the database
            admin.site.site_header = f"{about.title}'s Portfolio Admin"
            admin.site.site_title = f"{about.title}'s Portfolio"
        else:
            # Fallback if no AboutSection exists
            admin.site.site_header = "Portfolio Admin"
            admin.site.site_title = "Portfolio Admin"
    except:
        # Fallback in case of any errors (like during migrations)
        admin.site.site_header = "Portfolio Admin"
        admin.site.site_title = "Portfolio Admin"

admin.site.index_title = "Welcome to Portfolio Administration"

# We need to call this function only after the database is ready
# This is done through the ready() method in the AppConfig
