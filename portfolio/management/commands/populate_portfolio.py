from django.core.management.base import BaseCommand
from django.utils.text import slugify
from portfolio.models import (
    AboutSection, Skill, Project, Experience, Education
)
from datetime import date

class Command(BaseCommand):
    help = 'Populate portfolio with Vijay\'s resume data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate portfolio data...'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        AboutSection.objects.all().delete()
        Skill.objects.all().delete()
        Project.objects.all().delete()
        Experience.objects.all().delete()
        Education.objects.all().delete()

        # Create About Section
        self.stdout.write('Creating About section...')
        about = AboutSection.objects.create(
            title="About Vijay Tiwari",
            description="""I possess a strong command of SQL, Power BI, Tableau, Python, Advanced MS-Excel, and an array of tools within the MS-Office suite. My philosophy centers on delivering added value to every role I undertake. 

As a passionate Data Analyst with strong analytical skills, I am seeking challenging opportunities in Data Analysis to leverage my academic knowledge and gain practical experience in a professional setting. I believe in transforming raw data into meaningful insights that drive business decisions.

My experience includes data cleaning, preprocessing, quality analysis, and creating interactive dashboards and visualizations. I have successfully worked on various projects involving e-commerce analysis, literacy trends analysis, and crime data analysis, demonstrating my ability to extract valuable insights from complex datasets.""",
            email="Vijaydataanalyst91@gmail.com",
            phone="9131735630",
            location="Hyderabad, India",
            linkedin_url="https://linkedin.com/in/vijay-tiwari-data-analyst",
            github_url="https://github.com/vijaytiwari91",
            website_url="",
            profile_image="profile/vijay_profile.jpg"
        )

        # Create Skills
        self.stdout.write('Creating Skills...')
          # Programming & Database Skills
        programming_skills = [
            ('Python', 'programming', 'fab fa-python'),
            ('MySQL', 'database', 'fas fa-database'),
            ('SQL Server', 'database', 'fas fa-server'),
            ('SQLite3', 'database', 'fas fa-database'),
        ]

        # Data Science Libraries
        ds_skills = [
            ('Pandas', 'programming', 'fas fa-chart-line'),
            ('NumPy', 'programming', 'fas fa-calculator'),
            ('Matplotlib', 'programming', 'fas fa-chart-bar'),
            ('Seaborn', 'programming', 'fas fa-chart-area'),
        ]

        # Data Visualization Tools
        viz_skills = [
            ('Tableau', 'frontend', 'fas fa-chart-pie'),
            ('Power BI', 'frontend', 'fas fa-chart-line'),
            ('MS Excel', 'other', 'fas fa-file-excel'),
            ('VBA Macro', 'programming', 'fas fa-code'),
        ]

        # Other Technical Skills
        other_skills = [
            ('Data Cleaning', 'other', 'fas fa-broom'),
            ('Data Modeling', 'other', 'fas fa-project-diagram'),
            ('Data Visualization', 'other', 'fas fa-chart-bar'),
            ('Statistical Analysis', 'other', 'fas fa-calculator'),
            ('ETL Processes', 'other', 'fas fa-exchange-alt'),
            ('Dashboard Development', 'frontend', 'fas fa-tachometer-alt'),
        ]

        all_skills = programming_skills + ds_skills + viz_skills + other_skills
        
        for i, (name, category, icon) in enumerate(all_skills):
            is_featured = i < 8  # Make first 8 skills featured
            Skill.objects.create(
                name=name,
                category=category,
                icon=icon,
                is_featured=is_featured,
                order=i
            )

        # Create Education
        self.stdout.write('Creating Education...')
        Education.objects.create(
            institution_name="Swami Vivekanand University",
            degree="Bachelor of Computer Science Engineering",
            degree_type="bachelor",
            field_of_study="Computer Science Engineering",
            description="Comprehensive study of computer science fundamentals, programming, data structures, algorithms, and software engineering principles.",
            gpa="78%",
            start_date=date(2019, 6, 1),
            end_date=date(2023, 5, 31),
            location="India",
            is_current=False,
            order=1
        )

        Education.objects.create(
            institution_name="Govt Nehru High Secondary School",
            degree="Intermediate – 12th Standard",
            degree_type="other",
            field_of_study="Science",
            description="Higher Secondary Education with focus on Science subjects.",
            gpa="70%",
            start_date=date(2018, 6, 1),
            end_date=date(2019, 3, 31),
            location="India",
            is_current=False,
            order=2
        )

        Education.objects.create(
            institution_name="Govt Chandan Devi High School",
            degree="SSLC – 10th Standard",
            degree_type="other",
            field_of_study="General",
            description="Secondary School Leaving Certificate.",
            gpa="72%",
            start_date=date(2017, 6, 1),
            end_date=date(2018, 3, 31),
            location="India",
            is_current=False,
            order=3
        )

        # Create Work Experience
        self.stdout.write('Creating Work Experience...')
        
        # Get skills for relationships
        mysql_skill = Skill.objects.get(name='MySQL')
        excel_skill = Skill.objects.get(name='MS Excel')
        python_skill = Skill.objects.get(name='Python')
        tableau_skill = Skill.objects.get(name='Tableau')
        powerbi_skill = Skill.objects.get(name='Power BI')

        # Full-time experience
        exp1 = Experience.objects.create(
            company_name="Referenceglobe",
            position="Data Analyst",
            experience_type="work",
            description="""• Conducted data cleaning and preprocessing using MySQL queries and Excel
• Performed quality analysis of system products to ensure they meet high standards and requirements
• Assisted the development team in performing system health checks and verifying system functionality
• Provided effective technical support and troubleshooting, resolving issues promptly to maintain smooth CRM operations
• Delivered product demos to Heads of Departments (HODs), faculty, and Training and Placement Officers (TPOs)
• Gathered client requirements and coordinated with the development team to ensure needs are understood and addressed
• Used Excel to clean and prepare data before uploading it into the system
• Provided reports and visualizations through dashboards when additional insights or metrics were required
• Contributed to company efficiency through streamlined data management, improved system functionality, and enhanced user satisfaction""",
            start_date=date(2024, 2, 1),
            end_date=date(2024, 9, 30),
            location="India",
            is_current=False,
            order=1
        )
        exp1.technologies_used.set([mysql_skill, excel_skill, powerbi_skill])

        # Internship experience
        exp2 = Experience.objects.create(
            company_name="Skill Lync",
            position="Data Analyst Intern",
            experience_type="internship",
            description="""• Conducted research, analysis, and preparation of project reports for retail e-commerce projects
• Analyzed retail sales data transactions of e-commerce company with comprehensive data analysis
• Delivered interactive reports and dashboards for monitoring KPIs including Products, Orders, Sales, Profit, Quantity, Loss
• Created visualizations on Weekly, Monthly, Quarterly, and Yearly basis for business insights
• Successfully completed certification program in Data Analyst and Data Science internship
• Gained hands-on experience with real-world data analysis projects and industry best practices""",
            start_date=date(2023, 9, 1),
            end_date=date(2023, 11, 30),
            location="Chennai, India",
            is_current=False,
            order=2
        )
        exp2.technologies_used.set([python_skill, excel_skill, tableau_skill])

        # Create Projects
        self.stdout.write('Creating Projects...')
        
        # Project 1: E-commerce Analysis
        proj1 = Project.objects.create(
            title="E-Commerce User Analysis",
            slug="ecommerce-user-analysis",
            short_description="Comprehensive analysis of e-commerce user data with 98,913 rows and 27 columns to understand user behavior and preferences.",
            description="""This project involved analyzing user data for an e-commerce platform to gain insights into user behavior, demographics, and preferences. 

**Key Achievements:**
• Analyzed a comprehensive dataset containing 98,913 rows and 27 columns of user data
• Explored dataset structure and performed initial analysis to understand data quality and completeness
• Examined user demographics including age groups, geographic distribution, and user segments
• Analyzed follower counts and social engagement patterns to understand user influence
• Investigated user preferences, purchase patterns, and product interests
• Examined user engagement metrics, wish-list preferences, and platform usage
• Analyzed language usage patterns and regional preferences
• Provided actionable insights for improving user experience and targeted marketing strategies

**Technical Implementation:**
• Used SQL for data extraction, cleaning, and complex queries
• Performed statistical analysis to identify trends and patterns
• Created data models to segment users based on behavior and demographics
• Generated comprehensive reports with visualizations for stakeholder presentations

**Business Impact:**
• Identified key user segments for targeted marketing campaigns
• Provided insights for product recommendation improvements
• Helped optimize user engagement strategies based on demographic analysis""",
            project_type="data",
            live_url="",
            github_url="https://github.com/vijaytiwari91/ecommerce-analysis",
            demo_url="",
            is_featured=True,
            is_published=True,
            order=1
        )
        proj1.technologies.set([mysql_skill, excel_skill])

        # Project 2: Literacy Trends Analysis
        proj2 = Project.objects.create(
            title="Analyzing Literacy Trends in Tamil Nadu",
            slug="tamilnadu-literacy-analysis",
            short_description="Interactive Tableau dashboard analyzing literacy trends in Tamil Nadu from 2000-2011, highlighting gender disparities and population insights.",
            description="""A comprehensive analysis of literacy trends in Tamil Nadu using Tableau and Excel to create interactive visualizations and dashboards.

**Key Achievements:**
• Conducted comprehensive analysis of literacy trends showing significant improvements from 2000 to 2011
• Highlighted critical gender disparities in literacy rates across different regions
• Provided detailed population insights and demographic breakdowns
• Created interactive dashboard with innovative layout design for compelling data presentation
• Constructed robust visualization tool enabling informed decision-making for educational initiatives

**Technical Implementation:**
• Used Tableau for creating interactive dashboards and advanced visualizations
• Implemented Excel for data preprocessing and initial analysis
• Designed user-friendly interface with drill-down capabilities
• Created dynamic filters and parameters for customized analysis
• Developed trend analysis charts showing progress over time

**Visualization Features:**
• Interactive maps showing literacy rates by district
• Gender-wise literacy comparison charts
• Time-series analysis of literacy improvements
• Population density vs literacy correlation analysis
• Age group wise literacy distribution

**Business Impact:**
• Enabled government agencies to identify areas needing focused educational interventions
• Provided data-driven insights for policy makers to boost literacy rates
• Helped in resource allocation for educational programs
• Supported initiatives to address gender gaps in education""",
            project_type="data",
            live_url="",
            github_url="https://github.com/vijaytiwari91/tamilnadu-literacy",
            demo_url="",
            is_featured=True,
            is_published=True,
            order=2
        )
        proj2.technologies.set([tableau_skill, excel_skill])

        # Project 3: Crime Analysis
        proj3 = Project.objects.create(
            title="Crime Analysis in India",
            slug="india-crime-analysis",
            short_description="Python-based analysis of crime data in India using Pandas, focusing on data preprocessing, outlier removal, and statistical insights.",
            description="""A comprehensive crime data analysis project for India using Python and advanced data science techniques to extract meaningful insights.

**Key Achievements:**
• Collected and processed crime dataset from Kaggle.com with extensive data cleaning
• Performed complete ETL (Extract, Transform, Load) process on large-scale crime data
• Successfully removed outliers and handled null values to ensure data quality
• Presented insights on crime underrepresentation and reporting patterns
• Analyzed graduation trends and their correlation with crime rates
• Investigated educational disparities and their impact on crime statistics
• Conducted salary vs crime rate comparisons across different regions

**Technical Implementation:**
• Used Python for data manipulation and statistical analysis
• Implemented Pandas for data preprocessing and cleaning
• Applied advanced outlier detection and removal techniques
• Created data pipelines for automated data processing
• Performed statistical analysis and hypothesis testing

**Data Processing Techniques:**
• Handled missing data using multiple imputation methods
• Applied statistical outlier detection (IQR method, Z-score)
• Normalized data for comparative analysis across states
• Created derived variables for enhanced analysis

**Key Insights:**
• Identified patterns in crime reporting and underrepresentation
• Established correlations between education levels and crime rates
• Analyzed regional variations in crime patterns
• Provided recommendations for crime prevention strategies

**Deliverables:**
• Comprehensive PowerPoint presentation with key findings
• Statistical analysis reports with actionable insights
• Data visualization charts showing crime trends and patterns""",
            project_type="data",
            live_url="",
            github_url="https://github.com/vijaytiwari91/india-crime-analysis",
            demo_url="",
            is_featured=True,
            is_published=True,
            order=3
        )
        proj3.technologies.set([python_skill, Skill.objects.get(name='Pandas')])

        # Project 4: Vehicle Insurance EDA
        proj4 = Project.objects.create(
            title="EDA on Vehicle Insurance Customer Data",
            slug="vehicle-insurance-eda",
            short_description="Exploratory Data Analysis on Vehicle Insurance Customer Data using Python, Pandas, and Matplotlib for customer insights.",
            description="""Conducted comprehensive Exploratory Data Analysis (EDA) on Vehicle Insurance Customer Data to extract valuable business insights and customer behavior patterns.

**Key Achievements:**
• Performed comprehensive EDA on Vehicle Insurance Customer Data using Python and Pandas
• Demonstrated strong data cleaning and analytical skills with complex insurance datasets
• Implemented effective data preprocessing techniques to handle various data quality issues
• Extracted valuable insights from complex datasets for business decision making
• Created detailed customer segmentation analysis for targeted marketing strategies

**Technical Implementation:**
• Used Python as primary programming language for analysis
• Leveraged Pandas for data manipulation, cleaning, and analysis
• Implemented Matplotlib for creating insightful visualizations
• Applied statistical methods for customer behavior analysis
• Performed correlation analysis and feature engineering

**Data Analysis Techniques:**
• Univariate analysis of customer demographics and policy details
• Bivariate analysis to understand relationships between variables
• Customer segmentation based on policy preferences and demographics
• Churn analysis and risk assessment modeling
• Premium analysis and pricing optimization insights

**Key Insights Generated:**
• Customer demographic patterns and preferences
• Policy renewal and retention trends
• Risk factors affecting insurance claims
• Pricing optimization opportunities
• Customer lifetime value analysis

**Visualizations Created:**
• Distribution plots for customer demographics
• Correlation heatmaps for feature relationships
• Box plots for outlier detection and analysis
• Bar charts for categorical variable analysis
• Scatter plots for continuous variable relationships

**Business Impact:**
• Provided actionable insights for customer retention strategies
• Identified opportunities for cross-selling and upselling
• Helped optimize pricing strategies based on risk analysis
• Supported development of targeted marketing campaigns""",
            project_type="data",
            live_url="",
            github_url="https://github.com/vijaytiwari91/vehicle-insurance-eda",
            demo_url="",
            is_featured=True,
            is_published=True,
            order=4
        )
        proj4.technologies.set([python_skill, Skill.objects.get(name='Pandas'), Skill.objects.get(name='Matplotlib')])

        self.stdout.write(
            self.style.SUCCESS('Successfully populated portfolio with Vijay\'s data!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Created:')
        )
        self.stdout.write(f'- 1 About section')
        self.stdout.write(f'- {Skill.objects.count()} Skills')
        self.stdout.write(f'- {Education.objects.count()} Education entries')
        self.stdout.write(f'- {Experience.objects.count()} Experience entries')
        self.stdout.write(f'- {Project.objects.count()} Projects')
