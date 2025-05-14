"""
Script to update all API URLs from port 8001 to port 8000 in the frontend codebase
"""
import os
import re
import sys

def update_api_urls(directory):
    """
    Recursively search for JavaScript files in the given directory
    and update all occurrences of 'http://localhost:8001/api/v1' to 'http://localhost:8000/api/v1'
    """
    pattern = r'http://localhost:8001/api/v1'
    replacement = r'http://localhost:8000/api/v1'
    
    # Count of files and replacements
    files_updated = 0
    replacements_made = 0
    
    # Walk through the directory tree
    for root, _, files in os.walk(directory):
        for file in files:
            # Only process JavaScript files
            if file.endswith('.js'):
                file_path = os.path.join(root, file)
                
                # Read the file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if the pattern exists in the file
                if pattern in content:
                    # Replace all occurrences
                    new_content = content.replace(pattern, replacement)
                    replacements_in_file = content.count(pattern)
                    
                    # Write the updated content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    print(f"Updated {file_path}: {replacements_in_file} replacements")
                    files_updated += 1
                    replacements_made += replacements_in_file
    
    return files_updated, replacements_made

if __name__ == "__main__":
    # Directory to search in
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend', 'src')
    
    print(f"Searching for API URLs to update in: {frontend_dir}")
    files_updated, replacements_made = update_api_urls(frontend_dir)
    
    print(f"\nSummary:")
    print(f"- Files updated: {files_updated}")
    print(f"- Total replacements made: {replacements_made}")
    
    if replacements_made > 0:
        print("\nAll API URLs have been updated from port 8001 to port 8000.")
        print("Please restart the frontend application for changes to take effect.")
    else:
        print("\nNo API URLs were found that needed updating.")
