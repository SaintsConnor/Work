Connect-MsolService
# Retrieve all users
$users = Get-MsolUser -All

# Create a custom object to hold the MFA status
$mfaStatus = @()

foreach ($user in $users) {
    $mfaState = @{}

    # Check if the user has MFA enabled
    $mfaState.UserPrincipalName = $user.UserPrincipalName
    $mfaState.DisplayName = $user.DisplayName

    # Get StrongAuthenticationRequirements to determine MFA status
    $mfaEnabled = $user.StrongAuthenticationRequirements.State
    
    if ($mfaEnabled -ne $null) {
        $mfaState.MFAStatus = "Enabled"
    } else {
        $mfaState.MFAStatus = "Disabled"
    }

    # Add user MFA status to the array
    $mfaStatus += New-Object PSObject -Property $mfaState
}

# Export the MFA status to a CSV file
$mfaStatus | Export-Csv -Path "C:\Exports\MFA_Status_Report.csv" -NoTypeInformation

# Output MFA status to the console
$mfaStatus
