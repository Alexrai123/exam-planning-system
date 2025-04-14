# PowerShell script to run the SQL script to add group leader

# Copy the SQL script to the Docker container
Write-Host "Copying SQL script to the Docker container..."
docker cp ./add_group_leader.sql exam_planning_db:/tmp/add_group_leader.sql

# Execute the SQL script
Write-Host "Executing the SQL script..."
docker exec exam_planning_db psql -U postgres -d exam_planning -f /tmp/add_group_leader.sql

# Restart the backend to apply changes
Write-Host "Restarting the backend..."
docker restart exam_planning_backend

Write-Host "Group leader functionality added!"
