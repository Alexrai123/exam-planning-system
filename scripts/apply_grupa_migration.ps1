# PowerShell script to apply grupa table migration

# Copy the migration file to the Docker container
Write-Host "Copying migration file to the Docker container..."
docker cp ./backend/migrations/update_grupa_id.sql exam_planning_db:/tmp/update_grupa_id.sql

# Create a backup before making changes
Write-Host "Creating a database backup before migration..."
docker exec exam_planning_db pg_dump -U postgres -d exam_planning > ./exam_planning_backup_before_grupa_change.sql

# Execute the migration script
Write-Host "Applying database migrations..."
docker exec exam_planning_db psql -U postgres -d exam_planning -f /tmp/update_grupa_id.sql

Write-Host "Migration completed! Restarting backend..."
docker restart exam_planning_backend

Write-Host "Done!"
