# PowerShell script to run the SQL script to restore user links

# Copy the SQL script to the Docker container
Write-Host "Copying SQL script to the Docker container..."
docker cp ./restore_user_links.sql exam_planning_db:/tmp/restore_user_links.sql

# Execute the SQL script
Write-Host "Executing the SQL script..."
docker exec exam_planning_db psql -U postgres -d exam_planning -f /tmp/restore_user_links.sql

# Restart the backend to apply changes
Write-Host "Restarting the backend..."
docker restart exam_planning_backend

Write-Host "User links restored!"
