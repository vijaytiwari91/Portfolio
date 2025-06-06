from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class AboutSection(models.Model):
    """Model for the About section of the portfolio"""
    title = models.CharField(max_length=200, default="About Me")
    description = models.TextField()
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return self.title

class Skill(models.Model):
    """Model for skills"""
    SKILL_CATEGORIES = [
        ('programming', 'Programming Languages'),
        ('frontend', 'Frontend Technologies'),
        ('backend', 'Backend Technologies'),
        ('database', 'Database'),
        ('devops', 'DevOps & Tools'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SKILL_CATEGORIES, default='other')
    icon = models.CharField(max_length=100, blank=True, help_text="Font Awesome icon class")
    order = models.IntegerField(default=0, help_text="Order for display")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return self.name

class Project(models.Model):
    """Model for portfolio projects"""
    PROJECT_TYPES = [
        ('web', 'Web Application'),
        ('mobile', 'Mobile Application'),
        ('desktop', 'Desktop Application'),
        ('api', 'API/Backend'),
        ('data', 'Data Science/ML'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=300, help_text="Brief description for project cards")
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='web')
    technologies = models.ManyToManyField(Skill, related_name='projects', blank=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    live_url = models.URLField(blank=True, help_text="Live project URL")
    github_url = models.URLField(blank=True, help_text="GitHub repository URL")
    demo_url = models.URLField(blank=True, help_text="Demo/video URL")
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Order for display")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'order', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('portfolio:project_detail', kwargs={'slug': self.slug})

class Experience(models.Model):
    """Model for work experience"""
    EXPERIENCE_TYPES = [
        ('work', 'Work Experience'),
        ('internship', 'Internship'),
        ('freelance', 'Freelance'),
        ('volunteer', 'Volunteer'),
    ]

    company_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    experience_type = models.CharField(max_length=20, choices=EXPERIENCE_TYPES, default='work')
    description = models.TextField()
    technologies_used = models.ManyToManyField(Skill, related_name='experiences', blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Leave blank if current position")
    company_url = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_current = models.BooleanField(default=False)
    order = models.IntegerField(default=0, help_text="Order for display")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date', 'order']

    def __str__(self):
        return f"{self.position} at {self.company_name}"

    @property
    def duration(self):
        """Calculate duration of experience"""
        if self.end_date:
            return f"{self.start_date.strftime('%b %Y')} - {self.end_date.strftime('%b %Y')}"
        else:
            return f"{self.start_date.strftime('%b %Y')} - Present"

class Education(models.Model):
    """Model for education"""
    DEGREE_TYPES = [
        ('bachelor', "Bachelor's Degree"),
        ('master', "Master's Degree"),
        ('phd', 'PhD'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
        ('bootcamp', 'Bootcamp'),
        ('other', 'Other'),
    ]

    institution_name = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    degree_type = models.CharField(max_length=20, choices=DEGREE_TYPES, default='bachelor')
    field_of_study = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    gpa = models.CharField(max_length=10, blank=True, help_text="GPA or Grade")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    institution_url = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    is_current = models.BooleanField(default=False)
    order = models.IntegerField(default=0, help_text="Order for display")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date', 'order']

    def __str__(self):
        return f"{self.degree} - {self.institution_name}"

    @property
    def duration(self):
        """Calculate duration of education"""
        if self.end_date:
            return f"{self.start_date.strftime('%Y')} - {self.end_date.strftime('%Y')}"
        else:
            return f"{self.start_date.strftime('%Y')} - Present"

class ContactMessage(models.Model):
    """Model for contact form messages"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

# Create your models here.
