Write-Host "Adding April exam to the database..." -ForegroundColor Cyan

# Execute the SQL script inside the Docker container
Get-Content ./add_april_exam.sql | docker exec -i exam_planning_db psql -U postgres -d exam_planning

Write-Host "April exam added successfully!" -ForegroundColor Green
