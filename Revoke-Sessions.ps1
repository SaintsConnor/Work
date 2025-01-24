# Import required modules
Import-Module MSOnline
Import-Module AzureAD

# Set path to the CSV file
$csvPath = ".\users.csv"

# Authenticate to Microsoft 365
Write-Host "Connecting to Microsoft 365..." -ForegroundColor Green
$MsolSession = Connect-MsolService
$AzureSession = Connect-AzureAD

# Check if the CSV file exists
if (Test-Path $csvPath) {
    $users = Import-Csv -Path $csvPath

    foreach ($user in $users) {
        Write-Host "Raw Username from CSV: $($user.Username)" -ForegroundColor Cyan

        if (-not $user.Username) {
            Write-Host "Skipped: Missing username in CSV row." -ForegroundColor Red
            continue
        }

        $upn = $user.Username.Trim()  # Remove any leading/trailing spaces
        Write-Host "Processing user: $upn" -ForegroundColor Yellow

        try {
            # Retrieve Azure AD User
            $userObject = Get-AzureADUser -Filter "userPrincipalName eq '$upn'" -ErrorAction Stop

            if ($null -ne $userObject) {
                # Revoke Azure AD Refresh Tokens
                Revoke-AzureADUserAllRefreshToken -ObjectId $userObject.ObjectId
                Write-Host "Successfully logged off: $upn" -ForegroundColor Green
            } else {
                Write-Host "User not found in Azure AD: $upn" -ForegroundColor Red
            }
        } catch {
            Write-Host "Error processing user `${upn}: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
} else {
    Write-Host "CSV file not found at $csvPath. Please ensure the file exists." -ForegroundColor Red
}

# Disconnect sessions
Disconnect-MsolService
Write-Host "Script execution completed." -ForegroundColor Green

# Wait for user input before closing
Read-Host "Press Enter to close this script"
