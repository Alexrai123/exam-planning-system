# PowerShell script to run the additional schema changes

# Create a backup before making changes
Write-Host "Creating a database backup before making additional changes..."
docker exec exam_planning_db pg_dump -U postgres -d exam_planning > ./exam_planning_backup_before_additional_changes.sql

# Copy the SQL script to the Docker container
Write-Host "Copying SQL script to the Docker container..."
docker cp ./additional_schema_changes.sql exam_planning_db:/tmp/additional_schema_changes.sql

# Execute the SQL script
Write-Host "Executing the additional schema changes..."
docker exec exam_planning_db psql -U postgres -d exam_planning -f /tmp/additional_schema_changes.sql

# Restart the backend to apply changes
Write-Host "Restarting the backend..."
docker restart exam_planning_backend

Write-Host "Additional schema changes complete!"
