# PowerShell script to run the SQL script to update the leader field

# Copy the SQL script to the Docker container
Write-Host "Copying SQL script to the Docker container..."
docker cp ./update_leader_field.sql exam_planning_db:/tmp/update_leader_field.sql

# Execute the SQL script
Write-Host "Executing the SQL script..."
docker exec exam_planning_db psql -U postgres -d exam_planning -f /tmp/update_leader_field.sql

# Restart the backend to apply changes
Write-Host "Restarting the backend..."
docker restart exam_planning_backend

Write-Host "Leader field updated!"
