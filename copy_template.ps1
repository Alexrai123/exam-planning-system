# List of possible template locations
$locations = @(
    "C:\Users\Alex\Desktop\proiect gherman\backend\static\templates\exam_template.xlsx",
    "C:\Users\Alex\Desktop\proiect gherman\backend\app\templates\exam_template.xlsx",
    "C:\Users\Alex\Desktop\proiect gherman\backend\app\public\templates\exam_template.xlsx",
    "C:\Users\Alex\Desktop\proiect gherman\backend\output\updated_exam_template.xlsx"
)

$destinationFile = "C:\Users\Alex\Desktop\exam_template_updated.xlsx"
$found = $false

# Try each location
foreach ($location in $locations) {
    if (Test-Path $location) {
        Write-Host "Found template at: $location"
        Copy-Item -Path $location -Destination $destinationFile -Force
        Write-Host "Successfully copied template to: $destinationFile"
        $found = $true
        break
    }
}

if (-not $found) {
    Write-Host "Could not find template file in any location!"
}
