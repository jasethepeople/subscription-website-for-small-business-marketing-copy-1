import os
import json
from flask import Flask
from src.models.content import db, Template

def seed_templates(app):
    """Seed the database with initial content templates"""
    with app.app_context():
        # Check if templates already exist
        if Template.query.count() > 0:
            print("Templates already seeded, skipping...")
            return
        
        # Load template data from the markdown file
        template_file_path = os.path.join(os.path.dirname(__file__), 'templates', 'content_templates.md')
        
        with open(template_file_path, 'r') as file:
            content = file.read()
        
        # Extract JSON data from markdown
        social_templates_json = content.split('```json')[1].split('```')[0]
        email_templates_json = content.split('```json')[2].split('```')[0]
        ad_templates_json = content.split('```json')[3].split('```')[0]
        
        # Parse JSON data
        social_templates = json.loads(social_templates_json)
        email_templates = json.loads(email_templates_json)
        ad_templates = json.loads(ad_templates_json)
        
        # Combine all templates
        all_templates = social_templates + email_templates + ad_templates
        
        # Create template objects and add to database
        template_objects = []
        for template_data in all_templates:
            template = Template(
                category=template_data['category'],
                name=template_data['name'],
                description=template_data['description'],
                structure_json=template_data['structure_json'],
                thumbnail_url=template_data['thumbnail_url'],
                is_premium=template_data['is_premium']
            )
            template_objects.append(template)
        
        # Add all templates to database
        db.session.add_all(template_objects)
        db.session.commit()
        
        print(f"Successfully seeded {len(template_objects)} templates")

if __name__ == '__main__':
    # This script can be run directly to seed templates
    from src.main import app
    seed_templates(app)
