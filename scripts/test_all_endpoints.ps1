# PowerShell script to test all API endpoints

# Get the backend URL
$baseUrl = "http://localhost:8000"
$apiPrefix = "/api/v1"

# Function to make API requests and display results
function Test-Endpoint {
    param (
        [string]$Method,
        [string]$Endpoint,
        [string]$Description,
        [string]$Body = "",
        [string]$Token = "",
        [bool]$UseApiPrefix = $true,
        [bool]$IsFormData = $false
    )
    
    Write-Host "`n===== Testing: $Description ====="
    
    $fullUrl = if ($UseApiPrefix) { "$baseUrl$apiPrefix$Endpoint" } else { "$baseUrl$Endpoint" }
    Write-Host "$Method $fullUrl"
    
    $headers = @{}
    if ($Token -ne "") {
        $headers.Add("Authorization", "Bearer $Token")
    }
    
    try {
        if ($Method -eq "GET") {
            if ($Token -ne "") {
                $response = Invoke-RestMethod -Uri $fullUrl -Method $Method -Headers $headers -ErrorAction Stop
            } else {
                $response = Invoke-RestMethod -Uri $fullUrl -Method $Method -ErrorAction Stop
            }
        } else {
            if ($Body -ne "") {
                if ($IsFormData) {
                    # For form data
                    $headers.Add("Content-Type", "application/x-www-form-urlencoded")
                    $response = Invoke-RestMethod -Uri $fullUrl -Method $Method -Body $Body -Headers $headers -ErrorAction Stop
                } else {
                    # For JSON data
                    $response = Invoke-RestMethod -Uri $fullUrl -Method $Method -Body $Body -ContentType "application/json" -Headers $headers -ErrorAction Stop
                }
            } else {
                $response = Invoke-RestMethod -Uri $fullUrl -Method $Method -Headers $headers -ErrorAction Stop
            }
        }
        
        Write-Host "SUCCESS: $($response | ConvertTo-Json -Depth 3 -Compress)" -ForegroundColor Green
        return $response
    } catch {
        Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.ErrorDetails.Message) {
            Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
        }
        return $null
    }
}

# Start testing
Write-Host "Starting API endpoint tests..." -ForegroundColor Cyan

# Test root endpoint
Test-Endpoint -Method "GET" -Endpoint "/" -Description "Root endpoint" -UseApiPrefix $false

# Test authentication - using form data
$formData = "username=admin@example.com&password=password123"
$authResponse = Test-Endpoint -Method "POST" -Endpoint "/auth/login" -Description "Login as admin" -Body $formData -IsFormData $true

if ($authResponse) {
    $token = $authResponse.access_token
    Write-Host "Token obtained: $token" -ForegroundColor Yellow
    
    # Test users endpoints
    Test-Endpoint -Method "GET" -Endpoint "/users/" -Description "Get all users" -Token $token
    Test-Endpoint -Method "GET" -Endpoint "/users/1" -Description "Get user by ID" -Token $token
    
    # Test professors endpoints
    Test-Endpoint -Method "GET" -Endpoint "/professors/" -Description "Get all professors" -Token $token
    
    # Test groups endpoints
    Test-Endpoint -Method "GET" -Endpoint "/groups/" -Description "Get all groups" -Token $token
    Test-Endpoint -Method "GET" -Endpoint "/groups/CS101" -Description "Get group by name" -Token $token
    
    # Test rooms endpoints
    Test-Endpoint -Method "GET" -Endpoint "/rooms/" -Description "Get all rooms" -Token $token
    Test-Endpoint -Method "GET" -Endpoint "/rooms/A101" -Description "Get room by name" -Token $token
    
    # Test courses endpoints
    Test-Endpoint -Method "GET" -Endpoint "/courses/" -Description "Get all courses" -Token $token
    Test-Endpoint -Method "GET" -Endpoint "/courses/1" -Description "Get course by ID" -Token $token
    
    # Test exams endpoints
    Test-Endpoint -Method "GET" -Endpoint "/exams/" -Description "Get all exams" -Token $token
    Test-Endpoint -Method "GET" -Endpoint "/exams/1" -Description "Get exam by ID" -Token $token
    
    # Test filtering exams
    Test-Endpoint -Method "GET" -Endpoint "/exams/?grupa_name=CS101" -Description "Filter exams by group" -Token $token
    Test-Endpoint -Method "GET" -Endpoint "/exams/?sala_name=A101" -Description "Filter exams by room" -Token $token
    Test-Endpoint -Method "GET" -Endpoint "/exams/?status=PROPOSED" -Description "Filter exams by status" -Token $token
} else {
    Write-Host "Authentication failed, skipping protected endpoints" -ForegroundColor Red
}

Write-Host "`nAPI endpoint tests completed!" -ForegroundColor Cyan
