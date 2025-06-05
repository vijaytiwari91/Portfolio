import os
import sys
import django
import json
from datetime import datetime

# Set up Django environment
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

# Import models
from portfolio.models import Experience, Education, Skill

def fetch_experience():
    """Fetch all experience data and format it for the template"""
    experiences = Experience.objects.all().order_by('-is_current', '-start_date', 'order')
    experience_data = []
    
    for exp in experiences:
        # Get technologies used
        technologies = [{'id': tech.id, 'name': tech.name, 'icon': tech.icon} 
                       for tech in exp.technologies_used.all()]
        
        # Format date for better display
        duration = exp.duration
        
        experience_data.append({
            'id': exp.id,
            'position': exp.position,
            'company_name': exp.company_name,
            'experience_type': exp.experience_type,
            'experience_type_display': dict(Experience.EXPERIENCE_TYPES).get(exp.experience_type, ''),
            'description': exp.description,
            'start_date': exp.start_date.strftime('%Y-%m-%d'),
            'end_date': exp.end_date.strftime('%Y-%m-%d') if exp.end_date else None,
            'company_url': exp.company_url,
            'location': exp.location,
            'is_current': exp.is_current,
            'order': exp.order,
            'duration': duration,
            'technologies_used': technologies
        })
    
    return experience_data

def fetch_education():
    """Fetch all education data and format it for the template"""
    education_data = []
    education_entries = Education.objects.all().order_by('-is_current', '-start_date', 'order')
    
    for edu in education_entries:
        # Format date for better display
        duration = ""
        if edu.start_date and edu.end_date:
            duration = f"{edu.start_date.strftime('%b %Y')} - {edu.end_date.strftime('%b %Y')}"
        elif edu.start_date:
            duration = f"{edu.start_date.strftime('%b %Y')} - Present" if edu.is_current else f"{edu.start_date.strftime('%b %Y')} - "
        
        education_data.append({
            'id': edu.id,
            'institution_name': edu.institution_name,
            'degree': edu.degree,
            'degree_type': edu.degree_type,
            'degree_type_display': dict(Education.DEGREE_TYPES).get(edu.degree_type, ''),
            'field_of_study': edu.field_of_study,
            'description': edu.description,
            'gpa': edu.gpa,
            'start_date': edu.start_date.strftime('%Y-%m-%d'),
            'end_date': edu.end_date.strftime('%Y-%m-%d') if edu.end_date else None,
            'institution_url': edu.institution_url,
            'location': edu.location,
            'is_current': edu.is_current,
            'order': edu.order,
            'duration': duration
        })
    
    return education_data

if __name__ == "__main__":
    experience_data = fetch_experience()
    education_data = fetch_education()
    
    # Prepare data to render in the template
    template_data = {
        'experiences': experience_data,
        'education': education_data
    }
    
    print(json.dumps(template_data, indent=4))
    
    # Optionally write to a file
    with open('experience_data.json', 'w') as f:
        json.dump(template_data, f, indent=4)
    
    print(f"Fetched {len(experience_data)} experiences and {len(education_data)} education entries.")
