# PowerShell script to run the SQL script to populate the database

# Copy the SQL script to the Docker container
Write-Host "Copying SQL script to the Docker container..."
docker cp ./populate_database.sql exam_planning_db:/tmp/populate_database.sql

# Execute the SQL script
Write-Host "Executing the SQL script..."
docker exec exam_planning_db psql -U postgres -d exam_planning -f /tmp/populate_database.sql

Write-Host "Database populated with sample data!"
