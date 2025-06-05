# Portfolio Admin Dashboard - User Guide

## Overview
Your portfolio website now has a user-friendly admin dashboard that allows you to easily edit content directly through your website interface. No need to mess with complex admin panels or code!

## How to Access the Admin

### Method 1: Admin Menu (When Logged In)
1. Visit your website: http://127.0.0.1:8000
2. If you're logged in as an admin user, you'll see an "Admin" dropdown in the navigation menu
3. Click on "Admin" to see these options:
   - **Dashboard** - Main admin dashboard
   - **Edit About** - Quick edit your personal info
   - **Manage Projects** - Add/edit/organize projects
   - **Manage Skills** - Add/edit/organize skills
   - **Django Admin** - Access the full Django admin panel

### Method 2: Direct URLs
- Main Dashboard: http://127.0.0.1:8000/dashboard/
- Quick Edit About: http://127.0.0.1:8000/dashboard/about/edit/
- Manage Projects: http://127.0.0.1:8000/dashboard/projects/
- Manage Skills: http://127.0.0.1:8000/dashboard/skills/

## Dashboard Features

### 📊 Main Dashboard
- **Quick Statistics**: See counts of your projects, skills, and unread messages
- **Quick Actions**: Buttons for common tasks like editing about section or adding projects
- **Recent Content**: View your latest projects and unread contact messages
- **About Section Status**: Current state of your personal information

### 👤 Quick Edit About Section
- Update your name, description, location
- Change contact information (email, phone)
- Update social media links (LinkedIn, GitHub)
- Upload/change profile photo
- Preview changes instantly

### 📁 Manage Projects
- View all your projects in an organized layout
- **Toggle Featured Status**: Click the "Featured"/"Not Featured" buttons to control which projects appear on your homepage
- **Quick Actions**: Edit or view projects with one click
- **Visual Preview**: See project images and key information at a glance

### 🛠️ Manage Skills
- Organize skills by category (Programming, Frontend, Backend, etc.)
- **Toggle Featured Status**: Control which skills appear prominently on your homepage
- **Visual Organization**: Skills grouped by category for easy management
- **Quick Edit**: Edit skill details with one click

## Key Features

### ✨ Easy Content Management
- **No coding required** - Everything is done through user-friendly forms
- **Visual feedback** - See images and previews of your content
- **One-click actions** - Toggle featured status, mark messages as read
- **Responsive design** - Works on desktop, tablet, and mobile

### 🎨 Modern Interface
- Clean, professional design
- Intuitive navigation
- Hover effects and smooth animations
- Clear visual hierarchy

### ⚡ Quick Actions
- **Featured Content**: Easily control what appears on your homepage
- **Instant Updates**: Changes reflect immediately on your website
- **Bulk Operations**: Manage multiple items efficiently

## Common Tasks

### Adding a New Project
1. Go to Dashboard → "Add New Project" button
2. Fill in project details (title, description, type)
3. Upload project image
4. Add relevant technologies/skills
5. Set GitHub/live URLs if available
6. Check "Featured" if you want it on homepage
7. Save

### Updating Your About Section
1. Go to Dashboard → "Edit About Section"
2. Update any information you want to change
3. Upload new profile photo if desired
4. Save changes
5. Preview your website to see updates

### Managing Featured Content
1. Go to "Manage Projects" or "Manage Skills"
2. Click the toggle buttons to feature/unfeature items
3. Featured items appear prominently on your homepage
4. Changes are instant - no page refresh needed

### Handling Contact Messages
1. Check Dashboard for unread message count
2. Click "Mark as Read" on messages you've handled
3. Or go to Django Admin → Contact Messages for detailed view

## Tips for Best Results

### 📸 Images
- Use high-quality images for projects and profile photo
- Recommended sizes: Profile photo (400x400px), Project images (800x600px)
- Use PNG or JPG format

### 📝 Content Writing
- Keep project descriptions concise but informative
- Use action words in your about section
- Update contact information regularly

### 🎯 Featured Content Strategy
- Feature 3-6 of your best projects on homepage
- Feature 6-8 core skills to avoid clutter
- Regularly update featured content to keep site fresh

### 🔧 Technical Notes
- Always test changes by previewing your website
- Use the "Advanced Edit" option for complex changes
- Keep backups of important files (resume, project images)

## Troubleshooting

### Can't See Admin Menu?
- Make sure you're logged in with an admin account
- The menu only appears for staff users

### Changes Not Showing?
- Hard refresh your browser (Ctrl+F5)
- Clear browser cache
- Check if the item is published (for projects)

### Upload Issues?
- Check file size (images should be < 5MB)
- Use supported formats (JPG, PNG, PDF for resume)
- Ensure file names don't have special characters

## Security Notes
- Only admin users can access the dashboard
- Always log out when using shared computers
- Keep your admin password secure
- Regular backups are recommended

## Need Help?
- For basic content updates: Use the dashboard
- For advanced customization: Use Django Admin
- For technical issues: Check the terminal/console for error messages

---

**Happy editing! Your portfolio is now much easier to manage.** 🚀
