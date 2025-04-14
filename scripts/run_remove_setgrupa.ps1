# PowerShell script to run the SQL script to remove setGrupa_name

# Copy the SQL script to the Docker container
Write-Host "Copying SQL script to the Docker container..."
docker cp ./remove_setgrupa_name.sql exam_planning_db:/tmp/remove_setgrupa_name.sql

# Execute the SQL script
Write-Host "Executing the SQL script..."
docker exec exam_planning_db psql -U postgres -d exam_planning -f /tmp/remove_setgrupa_name.sql

# Restart the backend to apply changes
Write-Host "Restarting the backend..."
docker restart exam_planning_backend

Write-Host "Done!"
