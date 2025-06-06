import streamlit as st
import base64

# Page Configuration
st.set_page_config(
    page_title="Vijay Tiwari - Data Analyst Portfolio",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main styles */
    .main {
        padding: 0rem 5rem;
        background-color: #f8f9fa;
    }
    
    /* Custom container */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Profile image styling */
    .stImage {
        border-radius: 50%;
        border: 4px solid #1976d2;
        box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3);
        margin-bottom: 2rem;
        transition: transform 0.3s ease;
    }
    
    .stImage:hover {
        transform: scale(1.05);
    }
    
    /* Title and subtitle */
    .title-text {
        font-size: 48px !important;
        font-weight: bold;
        background: linear-gradient(120deg, #1a237e, #0d47a1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 20px;
        padding: 20px 0;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    .subtitle-text {
        font-size: 24px !important;
        color: #1976d2;
        text-align: center;
        margin-bottom: 50px;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* Section headers */
    .section-header {
        font-size: 28px !important;
        font-weight: bold;
        color: #1565c0;
        margin-top: 40px;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #bbdefb;
    }
    
    /* Content text */
    .content-text {
        font-size: 18px !important;
        color: #37474f;
        text-align: justify;
        line-height: 1.6;
    }
    
    /* Custom styling for markdown */
    .stMarkdown {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Link styling */
    a {
        color: #1976d2 !important;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    a:hover {
        color: #2196f3 !important;
        text-decoration: underline;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #e3f2fd !important;
        border-radius: 5px;
        padding: 10px !important;
        font-weight: bold !important;
    }
    
    .streamlit-expanderContent {
        background-color: white;
        border: 1px solid #bbdefb;
        border-radius: 0 0 5px 5px;
        padding: 15px !important;
    }
    
    /* Custom headers */
    h1, h2, h3 {
        color: #0d47a1 !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    h2 {
        border-bottom: 2px solid #bbdefb;
        padding-bottom: 10px;
        margin-top: 30px;
    }
    
    /* List styling */
    ul {
        list-style-type: none;
        padding-left: 0;
    }
    
    li {
        padding: 8px 0;
        margin-bottom: 5px;
        color: #37474f;
    }
    
    /* Column container styling */
    div.row-widget.stHorizontal {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    }
    
    /* Footer styling */
    footer {
        background: linear-gradient(120deg, #1a237e, #0d47a1);
        color: white !important;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        margin-top: 50px;
    }
    
    /* Custom button styling */
    .stButton button {
        background-color: #1976d2;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        transition: background-color 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #1565c0;
    }
    </style>
    """, unsafe_allow_html=True)

# Header Section
st.markdown('<p class="title-text">VIJAY TIWARI</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">Data Analyst with Strong Analytical Skills and Passion for Data Analytics</p>', unsafe_allow_html=True)

# Adding profile image
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("Image.jpg", width=300, caption="", use_column_width=False)

# Create columns for contact information
col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.markdown("### 📞 Contact")
    st.write("**Phone:** 9131735630")
    st.write("**Email:** Vijaydataanalyst91@gmail.com")

with col2:
    st.markdown("### 🌐 Social")
    st.markdown("[GitHub](https://github.com/vijaytiwari91)")
    st.markdown("[LinkedIn](Profile Link)")

with col3:
    st.markdown("### 📍 Location")
    st.write("**Base:** Hyderabad")

# Profile Section
st.markdown("## 📋 Profile")
st.write("I possess a strong command of SQL, Power BI, Tableau, Python, Advanced MS-Excel, and an array of tools within the MS-Office suite. My philosophy centers on delivering added value to every role I undertake. Seeking a challenging entry-level position in Data Analysis to leverage academic knowledge and gain practical experience in a professional setting.")

# Technical Skills Section
st.markdown("## 💻 Technical Skills")

# Create three columns for skills
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Programming & Database")
    st.markdown("""
    - **Python:** Matplotlib, Seaborn, Pandas, NumPy, SQLite3
    - **MySQL:** CRUD Operations, Stored procedures, CTEs, Views
    """)

with col2:
    st.markdown("### Data Visualization & Analytics")
    st.markdown("""
    - **Tableau:** Dashboards & Stories, Parameters, Actions
    - **Power BI:** Power Query Editor, Data Modelling
    - **MS Excel:** Advanced Features, Macros, VBA
    """)

with col3:
    st.markdown("### Soft Skills")
    st.markdown("""
    - Analytical thinking
    - Problem-solving
    - Team collaboration
    - Data modelling
    - Data visualization
    """)

# Education Section
st.markdown("## 🎓 Education")
st.markdown("""
- **Bachelor of Computer Science Engineering** (2019-2023)  
  Swami Vivekanand University | 78%

- **Intermediate – 12th Standard** (2018-2019)  
  Govt Nehru High Secondary School | 70%

- **SSLC – 10th Standard** (2017-2018)  
  Govt Chandan Devi High School | 72%
""")

# Work Experience Section
st.markdown("## 💼 Work Experience")
st.markdown("### Data Analyst | Referenceglobe")
st.markdown("*February 2024 – September 2024*")
st.markdown("""
- Conducted data cleaning and preprocessing using MySQL queries and Excel
- Performed quality analysis of system products
- Assisted in system health checks and functionality verification
- Provided technical support and troubleshooting
- Delivered product demos to stakeholders
- Created reports and visualizations through dashboards
""")

# Projects Section
st.markdown("## 🚀 Projects")

# Create expandable sections for each project
with st.expander("E-COMMERCE USER ANALYSIS - [SQL]"):
    st.markdown("""
    - Analyzed user data for an e-commerce platform (98,913 rows × 27 columns)
    - Explored dataset structure and performed initial analysis
    - Examined user demographics, follower counts, and preferences
    - Analyzed user engagement and wish-list preferences
    """)

with st.expander("ANALYSING LITERACY TRENDS IN TAMILNADU - [TABLEAU | EXCEL]"):
    st.markdown("""
    - Conducted comprehensive analysis of literacy trends (2000-2011)
    - Emphasized gender disparities and population insights
    - Created interactive dashboard with innovative layout
    - Built visualization tool for informed decision-making
    """)

with st.expander("CRIME ANALYSIS IN INDIA - [PYTHON | POWER POINT | PANDAS]"):
    st.markdown("""
    - Collected and processed dataset from Kaggle.com
    - Performed ETL operations and data cleaning
    - Analyzed crime patterns and trends
    - Created comprehensive visualizations and insights
    """)

with st.expander("EDA on VEHICLE INSURANCE CUSTOMER"):
    st.markdown("""
    - Conducted comprehensive EDA on Vehicle Insurance Data
    - Applied data cleaning and preprocessing techniques
    - Generated valuable insights from complex datasets
    - Created visualization for pattern recognition
    """)

# Certifications Section
st.markdown("## 🏆 Certifications")
st.markdown("""
- Data Analyst Certification by Skill-Lync (August 2023)
- Data Science Internship with Skill-Lync
""")

# Languages Section
st.markdown("## 🗣️ Languages")
st.markdown("""
- **Hindi:** Native Proficiency
- **English:** Professional Proficiency
""")

# Footer
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: #7f8c8d;'>
    © 2024 Vijay Tiwari - Data Analyst Portfolio
</p>
""", unsafe_allow_html=True)
