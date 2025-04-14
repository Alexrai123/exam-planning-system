# Script to add new fields to the courses table

Write-Host "Adding year, semester, and description fields to courses table..."

# Get the current directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$rootPath = Split-Path -Parent $scriptPath
$sqlPath = Join-Path -Path $rootPath -ChildPath "sql\add_course_fields.sql"

# Run the SQL script inside the Docker container
docker exec -i exam_planning_db psql -U postgres -d exam_planning -c "$(Get-Content -Path $sqlPath -Raw)"

if ($LASTEXITCODE -eq 0) {
    Write-Host "Successfully added new fields to courses table!" -ForegroundColor Green
} else {
    Write-Host "Failed to add new fields to courses table." -ForegroundColor Red
}
