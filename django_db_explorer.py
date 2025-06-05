# Django Database Explorer
# Run this in Django shell: python manage.py shell

from django.db import connection
from django.apps import apps
import sqlite3

def show_all_django_models():
    """Show all Django models in your project"""
    print("=== ALL DJANGO MODELS ===\n")
    
    for app_config in apps.get_app_configs():
        app_name = app_config.name
        models = app_config.get_models()
        
        if models:
            print(f"App: {app_name}")
            for model in models:
                model_name = model.__name__
                table_name = model._meta.db_table
                print(f"  • Model: {model_name} → Table: {table_name}")
            print()

def show_table_data_django(model_class):
    """Show data using Django ORM"""
    print(f"=== DATA FROM {model_class.__name__} ===\n")
    
    # Get all objects
    objects = model_class.objects.all()
    count = objects.count()
    
    print(f"Total records: {count}")
    
    if count > 0:
        print("\nFirst 5 records:")
        for i, obj in enumerate(objects[:5]):
            print(f"{i+1}. {obj}")
            # Show all field values
            for field in model_class._meta.fields:
                field_name = field.name
                field_value = getattr(obj, field_name)
                print(f"   {field_name}: {field_value}")
            print()

def execute_raw_sql(query):
    """Execute raw SQL query"""
    with connection.cursor() as cursor:
        cursor.execute(query)
        
        if query.strip().upper().startswith('SELECT'):
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()
            
            print("Columns:", columns)
            print("-" * 50)
            for row in rows:
                print(row)
        else:
            print("Query executed successfully")

# Example usage functions you can run in Django shell:

def explore_user_data():
    """Explore user-related data"""
    from django.contrib.auth.models import User
    
    print("=== USER DATA ===")
    users = User.objects.all()
    
    for user in users:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"First Name: {user.first_name}")
        print(f"Last Name: {user.last_name}")
        print(f"Date Joined: {user.date_joined}")
        print(f"Is Staff: {user.is_staff}")
        print(f"Is Active: {user.is_active}")
        print("-" * 30)

def explore_portfolio_models():
    """Explore your portfolio app models"""
    # Import your portfolio models here
    # For example:
    # from portfolio.models import Project, Skill, Contact
    
    # You'll need to replace these with your actual model names
    print("To use this function, uncomment and modify with your actual models:")
    print("from portfolio.models import YourModel")
    print("YourModel.objects.all()")

# Simple queries you can run in Django shell
def useful_queries():
    """Some useful queries to run"""
    
    print("=== USEFUL DJANGO SHELL COMMANDS ===\n")
    
    commands = [
        "# Show all users",
        "from django.contrib.auth.models import User",
        "User.objects.all()",
        "",
        "# Count users",
        "User.objects.count()",
        "",
        "# Get specific user",
        "User.objects.get(username='your_username')",
        "",
        "# Show your models",
        "from portfolio.models import *  # Import your models",
        "# Then use: ModelName.objects.all()",
        "",
        "# Raw SQL queries",
        "from django.db import connection",
        "cursor = connection.cursor()",
        "cursor.execute('SELECT * FROM auth_user LIMIT 5')",
        "cursor.fetchall()",
        "",
        "# Show all tables",
        "cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table';\")",
        "cursor.fetchall()"
    ]
    
    for cmd in commands:
        print(cmd)

if __name__ == "__main__":
    print("This script should be run in Django shell:")
    print("python manage.py shell")
    print("Then copy and paste these functions")
    useful_queries()