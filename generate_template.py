"""
Generate updated exam template with removed fields
"""
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import the template generator
from app.templates.exam_template import generate_exam_template

# Generate the template
output = generate_exam_template()

# Save to desktop with a new filename
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_file = os.path.join(desktop_path, "exam_template_reordered.xlsx")

with open(output_file, 'wb') as f:
    f.write(output.getvalue())

print(f"Template generated and saved to: {output_file}")
