# Ensure the Active Directory module is imported
Import-Module ActiveDirectory

# Define the output file location
$outputFile = "C:\Users\Public\Documents\ADUsers.csv"

# Export all Active Directory users
Get-ADUser -Filter * -Property DisplayName, EmailAddress, Department, Title, UserPrincipalName | 
Select-Object DisplayName, EmailAddress, Department, Title, UserPrincipalName | 
Export-Csv -Path $outputFile -NoTypeInformation

# Notify the user
Write-Host "Export completed. The CSV file is saved at $outputFile"
