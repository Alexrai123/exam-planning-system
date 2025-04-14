# PowerShell script to apply database migrations

# Copy the migration file to the Docker container
Write-Host "Copying migration file to the Docker container..."
docker cp ./backend/migrations/add_fields.sql exam_planning_db:/tmp/add_fields.sql

# Execute the migration script
Write-Host "Applying database migrations..."
docker exec exam_planning_db psql -U postgres -d exam_planning -f /tmp/add_fields.sql

Write-Host "Migration completed!"
