'''import os
import pdfkit
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

def generate_resume(resume_data):
    """Generate resume PDF from template and data"""
    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))
    
    # Select template
    template_name = f"{resume_data['template']}.html"
    template = env.get_template(template_name)
    
    # Render template with data
    rendered_html = template.render(resume_data)
    
    # Create PDF
    output_filename = f"generated_resume_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdfkit.from_string(rendered_html, output_filename)
    
    return output_filename'''
import os
import pdfkit
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import base64

def generate_resume(resume_data):
    """Generate resume PDF from template and data"""
    try:
        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader('templates'))
        
        # Select template
        template_name = f"{resume_data['template']}.html"
        template = env.get_template(template_name)
        
        # Prepare data for template
        template_data = {
            "personal_info": resume_data["personal_info"],
            "summary": resume_data["summary"],
            "experiences": resume_data["experiences"],
            "education": resume_data["education"],
            "skills": resume_data["skills"],
            "projects": resume_data["projects"],
            "certifications": resume_data.get("certifications", []),
            "languages": resume_data.get("languages", [])
        }
        
        # Add summary to personal_info if needed for some templates
        if "summary" in resume_data:
            template_data["personal_info"]["summary"] = resume_data["summary"]
        
        # Render template with data
        rendered_html = template.render(template_data)
        
        # PDF options
        options = {
            'page-size': 'A4',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'encoding': 'UTF-8',
            'quiet': '',
            'enable-local-file-access': None
        }
        
        # Create PDF
        output_filename = f"generated_resume_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdfkit.from_string(rendered_html, output_filename, options=options)
        
        return output_filename
    except Exception as e:
        print(f"Error generating resume: {str(e)}")
        raise e