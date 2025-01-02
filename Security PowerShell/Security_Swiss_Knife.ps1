# This script provides a group of security-related tasks
# You may need administrator privileges to execute some features.

function Get-LogonEvents {
    param ($EventId)
    $logName = "Security"

    Write-Output "Fetching log events for Event ID: $EventId. This may take a moment..."
    try {
        $events = Get-WinEvent -LogName $logName -FilterXPath "*[System/EventID=$EventId]" -ErrorAction Stop

        if ($events.Count -eq 0) {
            Write-Output "No events found."
        } else {
            $events | ForEach-Object {
                $eventDetails = $_ | Select-Object -ExpandProperty Properties

                $userName = $eventDetails[5].Value
                $timestamp = $_.TimeCreated

                [PSCustomObject]@{
                    UserName   = $userName
                    Timestamp  = $timestamp
                }
            } | Format-Table -AutoSize
        }
    } catch {
        Write-Error "An error occurred while fetching log events: $_"
    }
}

function MonitorFailedLogons {
    Get-LogonEvents -EventId 4625
}

function MonitorOpenPorts {
    Get-NetTCPConnection | Where-Object { $_.State -eq "Listen" } | Select LocalAddress, LocalPort | Format-Table -AutoSize
}

function ListFirewallRules {
    Get-NetFirewallRule | Where-Object { $_.Enabled -eq $true } | Select DisplayName, Direction, Action | Format-Table -AutoSize
}

function InactiveAccounts {
    Search-ADAccount -AccountInactive -UsersOnly -TimeSpan 90 | Select Name, LastLogonDate | Format-Table -AutoSize
}

function PasswordExpirationCheck {
    Get-ADUser -Filter * -Properties Name, PasswordLastSet | Where-Object {
        ($_.PasswordLastSet -lt (Get-Date).AddDays(-80))
    } | Select Name, PasswordLastSet | Format-Table -AutoSize
}

function KillMaliciousProcesses {
    $processName = Read-Host "Enter the name of the process to terminate"
    try {
        Get-Process -Name $processName | Stop-Process -Force
        Write-Output "Process $processName terminated."
    } catch {
        Write-Error ("Failed to terminate process " + $processName + ": " + $_)
    }
}

function CaptureSystemInfo {
    $outputDir = Read-Host "Enter the directory to save system information"
    if (-Not (Test-Path $outputDir)) {
        New-Item -ItemType Directory -Path $outputDir
    }

    Get-Process > "$outputDir\process_list.txt"
    Get-NetIPAddress > "$outputDir\network_info.txt"
    Write-Output "System information saved to $outputDir."
}

function ArchiveAndClearLogs {
    $logName = "Security"
    $archivePath = Read-Host "Enter the path to save the archived log file"

    try {
        wevtutil epl $logName $archivePath
        Write-Output "Log archived to $archivePath."

        wevtutil cl $logName
        Write-Output "$logName log cleared."
    } catch {
        Write-Error "Failed to archive or clear logs: $_"
    }
}

function MainMenu {
    Write-Output "Choose a security task to perform:"
    Write-Output "1. Monitor Logins"
    Write-Output "2. Active Directory Security"
    Write-Output "3. Network Security"
    Write-Output "4. Incident Response"
    Write-Output "5. Log Archiving and Cleanup"

    $choice = Read-Host "Enter your choice (1-5)"

    switch ($choice) {
        1 {
            Write-Output "1. Successful Logons (Event ID 4624)"
            Write-Output "2. Failed Logons (Event ID 4625)"
            $logChoice = Read-Host "Enter your choice"

            switch ($logChoice) {
                1 { Get-LogonEvents -EventId 4624 }
                2 { MonitorFailedLogons }
                Default { Write-Output "Invalid choice." }
            }
        }
        2 {
            Write-Output "1. List Inactive Accounts"
            Write-Output "2. Check Password Expiration"
            $adChoice = Read-Host "Enter your choice"

            switch ($adChoice) {
                1 { InactiveAccounts }
                2 { PasswordExpirationCheck }
                Default { Write-Output "Invalid choice." }
            }
        }
        3 {
            Write-Output "1. Monitor Open Ports"
            Write-Output "2. List Firewall Rules"
            $netChoice = Read-Host "Enter your choice"

            switch ($netChoice) {
                1 { MonitorOpenPorts }
                2 { ListFirewallRules }
                Default { Write-Output "Invalid choice." }
            }
        }
        4 {
            Write-Output "1. Kill Malicious Processes"
            Write-Output "2. Capture System Info"
            $irChoice = Read-Host "Enter your choice"

            switch ($irChoice) {
                1 { KillMaliciousProcesses }
                2 { CaptureSystemInfo }
                Default { Write-Output "Invalid choice." }
            }
        }
        5 {
            ArchiveAndClearLogs
        }
        Default { Write-Output "Invalid choice." }
    }
}

# Run the main menu
MainMenu
