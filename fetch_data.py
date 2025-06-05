#!/usr/bin/env python
# filepath: c:\Code\Hobbies\Portfolio-Vijay\fetch_data.py

import os
import sys
import django
import json
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

# Import models after Django setup
from portfolio.models import AboutSection, Skill, Project, Experience, Education, ContactMessage
from django.contrib.auth.models import User

# Helper function to convert date objects to string
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def fetch_all_data():
    """Fetch all data from the SQLite3 database and print it"""
    
    # Create a dictionary to hold all data
    all_data = {}
    
    # Fetch Users
    users = User.objects.all()
    all_data['users'] = list(users.values())
    print(f"Found {len(users)} users")
    
    # Fetch AboutSection
    about_sections = AboutSection.objects.all()
    all_data['about_sections'] = list(about_sections.values())
    print(f"Found {len(about_sections)} about sections")
    
    # Fetch Skills
    skills = Skill.objects.all()
    all_data['skills'] = list(skills.values())
    print(f"Found {len(skills)} skills")
    
    # Fetch Projects with related skills
    projects = Project.objects.all()
    projects_data = []
    for project in projects:
        project_dict = {
            'id': project.id,
            'title': project.title,
            'slug': project.slug,
            'description': project.description,
            'short_description': project.short_description,
            'project_type': project.project_type,
            'image': str(project.image) if project.image else None,
            'live_url': project.live_url,
            'github_url': project.github_url,
            'demo_url': project.demo_url,
            'is_featured': project.is_featured,
            'is_published': project.is_published,
            'order': project.order,
            'created_at': project.created_at,
            'updated_at': project.updated_at,
            'technologies': list(project.technologies.values('id', 'name', 'category'))
        }
        projects_data.append(project_dict)
    all_data['projects'] = projects_data
    print(f"Found {len(projects)} projects")
    
    # Fetch Experiences with related skills
    experiences = Experience.objects.all()
    experiences_data = []
    for experience in experiences:
        experience_dict = {
            'id': experience.id,
            'company_name': experience.company_name,
            'position': experience.position,
            'experience_type': experience.experience_type,
            'description': experience.description,
            'start_date': experience.start_date,
            'end_date': experience.end_date,
            'company_url': experience.company_url,
            'location': experience.location,
            'is_current': experience.is_current,
            'order': experience.order,
            'created_at': experience.created_at,
            'duration': experience.duration,
            'technologies_used': list(experience.technologies_used.values('id', 'name', 'category'))
        }
        experiences_data.append(experience_dict)
    all_data['experiences'] = experiences_data
    print(f"Found {len(experiences)} experiences")
    
    # Fetch Education
    education_entries = Education.objects.all()
    all_data['education'] = list(education_entries.values())
    print(f"Found {len(education_entries)} education entries")
    
    # Fetch Contact Messages
    contact_messages = ContactMessage.objects.all()
    all_data['contact_messages'] = list(contact_messages.values())
    print(f"Found {len(contact_messages)} contact messages")
    
    # Save to JSON file
    with open('database_data.json', 'w') as f:
        json.dump(all_data, f, default=json_serial, indent=4)
    
    print("\nAll data has been fetched and saved to 'database_data.json'")
    
    # Print details of each table
    print("\n--- Detailed Data Summary ---")
    
    if users:
        print("\nUsers:")
        for user in users:
            print(f"  - {user.username} (ID: {user.id})")
    
    if about_sections:
        print("\nAbout Sections:")
        for about in about_sections:
            print(f"  - {about.title}")
    
    if skills:
        print("\nSkills by Category:")
        categories = {}
        for skill in skills:
            if skill.category not in categories:
                categories[skill.category] = []
            categories[skill.category].append(skill.name)
        
        for category, skills_list in categories.items():
            print(f"  - {category.capitalize()}: {', '.join(skills_list)}")
    
    if projects:
        print("\nProjects:")
        for project in projects:
            print(f"  - {project.title} ({project.project_type})")
            if project.technologies.exists():
                tech_names = [tech.name for tech in project.technologies.all()]
                print(f"    Technologies: {', '.join(tech_names)}")
    
    if experiences:
        print("\nExperiences:")
        for exp in experiences:
            print(f"  - {exp.position} at {exp.company_name} ({exp.duration})")
    
    if education_entries:
        print("\nEducation:")
        for edu in education_entries:
            print(f"  - {edu.degree} in {edu.field_of_study} from {edu.institution_name}")
    
    if contact_messages:
        print("\nContact Messages:")
        for msg in contact_messages:
            status = "Read" if msg.is_read else "Unread"
            print(f"  - {status}: {msg.subject} from {msg.name} ({msg.created_at.strftime('%Y-%m-%d')})")

if __name__ == "__main__":
    fetch_all_data()
