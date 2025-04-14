# PowerShell script to run the simple rebuild SQL script

# Create a backup before making changes
Write-Host "Creating a database backup before migration..."
docker exec exam_planning_db pg_dump -U postgres -d exam_planning > ./exam_planning_backup_before_simple_rebuild.sql

# Copy the SQL script to the Docker container
Write-Host "Copying SQL script to the Docker container..."
docker cp ./simple_rebuild.sql exam_planning_db:/tmp/simple_rebuild.sql

# Execute the SQL script
Write-Host "Executing the database rebuild script..."
docker exec exam_planning_db psql -U postgres -d exam_planning -f /tmp/simple_rebuild.sql

# Restart the backend to apply changes
Write-Host "Restarting the backend..."
docker restart exam_planning_backend

Write-Host "Database rebuild complete!"
