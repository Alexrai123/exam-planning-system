"""
Script to save the updated exam template to a static location
"""
import sys
import os
import shutil
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

def save_static_exam_template():
    """
    Save the updated exam template to a static location
    """
    try:
        # Source file (our updated template)
        source_file = Path(__file__).parent.parent / "output" / "updated_exam_template.xlsx"
        
        if not source_file.exists():
            print(f"Error: Source file not found: {source_file}")
            return
        
        # Create static directory if it doesn't exist
        static_dir = Path(__file__).parent.parent / "static"
        static_dir.mkdir(exist_ok=True)
        
        templates_dir = static_dir / "templates"
        templates_dir.mkdir(exist_ok=True)
        
        # Destination file (where the template will be served from)
        dest_file = templates_dir / "exam_template.xlsx"
        
        # Copy the file
        shutil.copy2(source_file, dest_file)
        
        print(f"Template copied from {source_file} to {dest_file}")
        
        # Now update the API to serve this static file
        api_file = Path(__file__).parent.parent / "app" / "api" / "endpoints" / "public_templates.py"
        
        if not api_file.exists():
            print(f"Error: API file not found: {api_file}")
            return
        
        # Read the API file
        with open(api_file, "r") as f:
            api_content = f.read()
        
        # Check if we need to modify the file
        if "static/templates/exam_template.xlsx" not in api_content:
            # Create backup
            backup_file = api_file.with_suffix(".py.bak")
            shutil.copy2(api_file, backup_file)
            print(f"Created backup of API file: {backup_file}")
            
            # Modify the API file to serve the static template
            modified_content = api_content.replace(
                "def download_exam_template_public():",
                """def download_exam_template_public():
    \"\"\"
    Download Excel template for exam data (public endpoint)
    \"\"\"
    try:
        print("Serving static exam template")
        static_template = Path(__file__).parent.parent.parent.parent / "static" / "templates" / "exam_template.xlsx"
        
        if static_template.exists():
            # Add CORS headers
            headers = {
                "Content-Disposition": "attachment; filename=exam_template.xlsx",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, OPTIONS",
                "Access-Control-Allow-Headers": "Authorization, Content-Type"
            }
            
            # Return the static file
            with open(static_template, "rb") as f:
                content = f.read()
            
            return StreamingResponse(
                io.BytesIO(content),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers=headers
            )
    except Exception as e:
        print(f"Error serving static exam template: {e}")
    
    # Fall back to generating the template dynamically
    try:
        print("Generating public exam template dynamically")"""
            )
            
            # Write the modified content
            with open(api_file, "w") as f:
                f.write(modified_content)
            
            print(f"Modified API file to serve static template: {api_file}")
        else:
            print("API file already modified to serve static template")
        
        print("\nDone! The updated exam template will now be served when downloading from the frontend.")
        print("You may need to restart the backend server for changes to take effect.")
        
    except Exception as e:
        print(f"Error saving static exam template: {e}")

if __name__ == "__main__":
    save_static_exam_template()
