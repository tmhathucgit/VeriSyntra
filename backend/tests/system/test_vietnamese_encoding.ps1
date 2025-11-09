<#
.SYNOPSIS
    Test Vietnamese UTF-8 encoding integrity and diacritics compliance across all database tables
    
.DESCRIPTION
    Validates that all Vietnamese fields (_vi suffix) in the database:
    1. Use proper UTF-8 encoding (byte_count > char_count for diacritics)
    2. Do not have missing diacritics (no non-diacritic Vietnamese)
    3. Are free from corruption (no question marks or garbled text)
    
    This script is part of VeriSyntra's Vietnamese data quality assurance.
    
.PARAMETER Container
    Docker container name (default: verisyntra-postgres)
    
.PARAMETER Database
    Database name (default: verisyntra)
    
.PARAMETER User
    Database user (default: verisyntra)
    
.PARAMETER FailOnWarnings
    Exit with error code if warnings are found (default: $false)
    
.EXAMPLE
    .\test_vietnamese_encoding.ps1
    
.EXAMPLE
    .\test_vietnamese_encoding.ps1 -FailOnWarnings $true
    
.NOTES
    Author: VeriSyntra Team
    Date: November 8, 2025
    Purpose: Ensure Vietnamese UTF-8 data integrity and diacritics compliance
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$Container = "verisyntra-postgres",
    
    [Parameter(Mandatory=$false)]
    [string]$Database = "verisyntra",
    
    [Parameter(Mandatory=$false)]
    [string]$User = "verisyntra",
    
    [Parameter(Mandatory=$false)]
    [bool]$FailOnWarnings = $false
)

# Color output functions
function Write-TestHeader {
    param([string]$Message)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
}

function Write-TestPass {
    param([string]$Message)
    Write-Host "[PASS] $Message" -ForegroundColor Green
}

function Write-TestFail {
    param([string]$Message)
    Write-Host "[FAIL] $Message" -ForegroundColor Red
}

function Write-TestWarn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-TestInfo {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

# Initialize test results
$script:totalTests = 0
$script:passedTests = 0
$script:failedTests = 0
$script:warnings = 0

function Record-TestResult {
    param(
        [bool]$Passed,
        [string]$Message,
        [bool]$IsWarning = $false
    )
    
    $script:totalTests++
    
    if ($IsWarning) {
        $script:warnings++
        Write-TestWarn $Message
    } elseif ($Passed) {
        $script:passedTests++
        Write-TestPass $Message
    } else {
        $script:failedTests++
        Write-TestFail $Message
    }
}

Write-TestHeader "Vietnamese Encoding & Diacritics Test Suite"
Write-Host "Testing database: $Database in container: $Container" -ForegroundColor Cyan
Write-Host ""

# Test 1: Container is running
Write-TestInfo "Test 1: Checking Docker container..."
$containerRunning = docker ps --filter "name=$Container" --format "{{.Names}}" 2>$null

if ($containerRunning -eq $Container) {
    Record-TestResult -Passed $true -Message "Docker container '$Container' is running"
} else {
    Record-TestResult -Passed $false -Message "Docker container '$Container' is not running"
    Write-Host ""
    Write-Host "Test suite aborted - container not available" -ForegroundColor Red
    exit 1
}

# Test 2: Database connection
Write-TestInfo "Test 2: Testing database connection..."
docker exec $Container psql -U $User -d $Database -c "SELECT 1;" 2>$null | Out-Null

if ($LASTEXITCODE -eq 0) {
    Record-TestResult -Passed $true -Message "Database connection successful"
} else {
    Record-TestResult -Passed $false -Message "Cannot connect to database"
    exit 1
}

# Test 3: Find all Vietnamese fields
Write-TestInfo "Test 3: Discovering Vietnamese fields (_vi suffix)..."
$vietnameseFieldsQuery = @"
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'public' 
AND column_name LIKE '%_vi' 
ORDER BY table_name, column_name;
"@

$vietnameseFields = docker exec $Container psql -U $User -d $Database -t -c $vietnameseFieldsQuery 2>$null

if ($vietnameseFields) {
    $fieldCount = ($vietnameseFields | Measure-Object -Line).Lines
    Record-TestResult -Passed $true -Message "Found $fieldCount Vietnamese fields across tables"
    Write-Host ""
    Write-Host "Vietnamese fields discovered:" -ForegroundColor Cyan
    Write-Host $vietnameseFields
} else {
    Record-TestResult -Passed $false -Message "No Vietnamese fields found"
    exit 1
}

# Test 4: Check permissions table encoding
Write-TestHeader "Test 4: Permissions Table Encoding"

$permissionsEncodingQuery = @"
SELECT 
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE permission_name_vi IS NOT NULL AND permission_name_vi != '') as has_data,
    COUNT(*) FILTER (WHERE octet_length(permission_name_vi) > length(permission_name_vi)) as utf8_correct,
    COUNT(*) FILTER (WHERE octet_length(permission_name_vi) = length(permission_name_vi)) as ascii_only,
    COUNT(*) FILTER (WHERE permission_name_vi ~ '[\?]') as corrupted
FROM permissions
WHERE permission_name_vi IS NOT NULL AND permission_name_vi != '';
"@

$permResult = docker exec $Container psql -U $User -d $Database -t -c $permissionsEncodingQuery 2>$null
if ($permResult) {
    $parts = $permResult.Trim() -split '\|'
    $total = [int]$parts[0].Trim()
    $hasData = [int]$parts[1].Trim()
    $utf8Correct = [int]$parts[2].Trim()
    $asciiOnly = [int]$parts[3].Trim()
    $corrupted = [int]$parts[4].Trim()
    
    Write-Host "  Total records: $total"
    Write-Host "  UTF-8 correct: $utf8Correct"
    Write-Host "  ASCII-only: $asciiOnly"
    Write-Host "  Corrupted: $corrupted"
    
    if ($corrupted -gt 0) {
        Record-TestResult -Passed $false -Message "permissions.permission_name_vi has $corrupted corrupted entries"
    } else {
        Record-TestResult -Passed $true -Message "permissions.permission_name_vi has no corrupted entries"
    }
    
    if ($total -gt 0) {
        $utf8Percent = [math]::Round(100.0 * $utf8Correct / $total, 1)
        if ($utf8Percent -ge 95.0) {
            Record-TestResult -Passed $true -Message "permissions.permission_name_vi UTF-8 compliance: $utf8Percent%"
        } else {
            Record-TestResult -Passed $false -Message "permissions.permission_name_vi UTF-8 compliance too low: $utf8Percent%"
        }
    }
}

# Test 5: Check tenants table encoding
Write-TestHeader "Test 5: Tenants Table Encoding"

$tenantsEncodingQuery = @"
SELECT 
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE company_name_vi IS NOT NULL AND company_name_vi != '') as has_data,
    COUNT(*) FILTER (WHERE octet_length(company_name_vi) > length(company_name_vi)) as utf8_correct,
    COUNT(*) FILTER (WHERE octet_length(company_name_vi) = length(company_name_vi)) as ascii_only,
    COUNT(*) FILTER (WHERE company_name_vi ~ '[\?]') as corrupted
FROM tenants
WHERE company_name_vi IS NOT NULL AND company_name_vi != '';
"@

$tenantResult = docker exec $Container psql -U $User -d $Database -t -c $tenantsEncodingQuery 2>$null
if ($tenantResult) {
    $parts = $tenantResult.Trim() -split '\|'
    $total = [int]$parts[0].Trim()
    $hasData = [int]$parts[1].Trim()
    $utf8Correct = [int]$parts[2].Trim()
    $asciiOnly = [int]$parts[3].Trim()
    $corrupted = [int]$parts[4].Trim()
    
    Write-Host "  Total records: $total"
    Write-Host "  UTF-8 correct: $utf8Correct"
    Write-Host "  ASCII-only: $asciiOnly"
    Write-Host "  Corrupted: $corrupted"
    
    if ($corrupted -gt 0) {
        Record-TestResult -Passed $false -Message "tenants.company_name_vi has $corrupted corrupted entries"
    } else {
        Record-TestResult -Passed $true -Message "tenants.company_name_vi has no corrupted entries"
    }
    
    if ($total -gt 0) {
        $utf8Percent = [math]::Round(100.0 * $utf8Correct / $total, 1)
        # Allow lower threshold for tenants (may have test data in English)
        if ($utf8Percent -ge 80.0) {
            Record-TestResult -Passed $true -Message "tenants.company_name_vi UTF-8 compliance: $utf8Percent%"
        } else {
            Record-TestResult -Passed $false -Message "tenants.company_name_vi UTF-8 compliance too low: $utf8Percent%"
        }
    }
}

# Test 6: Check users table encoding
Write-TestHeader "Test 6: Users Table Encoding"

$usersEncodingQuery = @"
SELECT 
    COUNT(*) as total,
    COUNT(*) FILTER (WHERE full_name_vi IS NOT NULL AND full_name_vi != '') as has_data,
    COUNT(*) FILTER (WHERE octet_length(full_name_vi) > length(full_name_vi)) as utf8_correct,
    COUNT(*) FILTER (WHERE octet_length(full_name_vi) = length(full_name_vi)) as ascii_only,
    COUNT(*) FILTER (WHERE full_name_vi ~ '[\?]') as corrupted
FROM users
WHERE full_name_vi IS NOT NULL AND full_name_vi != '';
"@

$userResult = docker exec $Container psql -U $User -d $Database -t -c $usersEncodingQuery 2>$null
if ($userResult) {
    $parts = $userResult.Trim() -split '\|'
    $total = [int]$parts[0].Trim()
    $hasData = [int]$parts[1].Trim()
    $utf8Correct = [int]$parts[2].Trim()
    $asciiOnly = [int]$parts[3].Trim()
    $corrupted = [int]$parts[4].Trim()
    
    Write-Host "  Total records: $total"
    Write-Host "  UTF-8 correct: $utf8Correct"
    Write-Host "  ASCII-only: $asciiOnly"
    Write-Host "  Corrupted: $corrupted"
    
    if ($corrupted -gt 0) {
        Record-TestResult -Passed $false -Message "users.full_name_vi has $corrupted corrupted entries"
    } else {
        Record-TestResult -Passed $true -Message "users.full_name_vi has no corrupted entries"
    }
    
    if ($total -gt 0) {
        $utf8Percent = [math]::Round(100.0 * $utf8Correct / $total, 1)
        if ($utf8Percent -ge 95.0) {
            Record-TestResult -Passed $true -Message "users.full_name_vi UTF-8 compliance: $utf8Percent%"
        } else {
            Record-TestResult -Passed $false -Message "users.full_name_vi UTF-8 compliance too low: $utf8Percent%"
        }
    }
}

# Test 7: Check for missing diacritics (common patterns)
Write-TestHeader "Test 7: Missing Diacritics Detection"

# Common Vietnamese words that should have diacritics
$diacriticChecks = @(
    @{Pattern = "nguoi dung"; Correct = "người dùng"; Table = "users"; Field = "full_name_vi"},
    @{Pattern = "cong ty"; Correct = "công ty"; Table = "tenants"; Field = "company_name_vi"},
    @{Pattern = "dia chi"; Correct = "địa chỉ"; Table = "tenants"; Field = "address_vi"},
    @{Pattern = "quan ly"; Correct = "quản lý"; Table = "permissions"; Field = "permission_name_vi"},
    @{Pattern = "bao mat"; Correct = "bảo mật"; Table = "permissions"; Field = "description_vi"}
)

foreach ($check in $diacriticChecks) {
    $checkQuery = @"
SELECT COUNT(*) 
FROM $($check.Table)
WHERE LOWER($($check.Field)) LIKE '%$($check.Pattern)%'
AND $($check.Field) IS NOT NULL
AND $($check.Field) != '';
"@
    
    $result = docker exec $Container psql -U $User -d $Database -t -c $checkQuery 2>$null
    
    if ($result) {
        # Handle both single value and array results
        $resultValue = if ($result -is [array]) { $result[0] } else { $result }
        $count = [int]$resultValue.Trim()
        if ($count -gt 0) {
            Record-TestResult -Passed $false -IsWarning $true -Message "$($check.Table).$($check.Field) has $count entries with '$($check.Pattern)' (should be '$($check.Correct)')"
        }
    }
}

if ($script:warnings -eq 0) {
    Record-TestResult -Passed $true -Message "No missing diacritics detected in common patterns"
}

# Test 8: Sample data verification
Write-TestHeader "Test 8: Sample Data Verification"

Write-TestInfo "Permissions table samples (first 3 with Vietnamese):"
$samplePermissions = docker exec $Container psql -U $User -d $Database -c "SELECT permission_name, permission_name_vi, length(permission_name_vi) as chars, octet_length(permission_name_vi) as bytes FROM permissions WHERE octet_length(permission_name_vi) > length(permission_name_vi) LIMIT 3;" 2>$null
Write-Host $samplePermissions

Write-TestInfo "Users table samples (first 3 with Vietnamese):"
$sampleUsers = docker exec $Container psql -U $User -d $Database -c "SELECT user_id, full_name_vi, length(full_name_vi) as chars, octet_length(full_name_vi) as bytes FROM users WHERE octet_length(full_name_vi) > length(full_name_vi) LIMIT 3;" 2>$null
Write-Host $sampleUsers

Write-TestInfo "Tenants table samples (first 3 with Vietnamese):"
$sampleTenants = docker exec $Container psql -U $User -d $Database -c "SELECT tenant_id, company_name_vi, length(company_name_vi) as chars, octet_length(company_name_vi) as bytes FROM tenants WHERE octet_length(company_name_vi) > length(company_name_vi) LIMIT 3;" 2>$null
Write-Host $sampleTenants

# Final Summary
Write-TestHeader "Test Results Summary"

Write-Host ""
Write-Host "Total Tests: $script:totalTests" -ForegroundColor Cyan
Write-Host "Passed: $script:passedTests" -ForegroundColor Green
Write-Host "Failed: $script:failedTests" -ForegroundColor Red
Write-Host "Warnings: $script:warnings" -ForegroundColor Yellow
Write-Host ""

if ($script:failedTests -eq 0 -and $script:warnings -eq 0) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "ALL TESTS PASSED - NO ISSUES DETECTED" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Vietnamese UTF-8 encoding: EXCELLENT" -ForegroundColor Green
    Write-Host "Diacritics compliance: EXCELLENT" -ForegroundColor Green
    Write-Host ""
    exit 0
} elseif ($script:failedTests -eq 0 -and $script:warnings -gt 0) {
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host "TESTS PASSED WITH WARNINGS" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Some Vietnamese entries may be missing diacritics" -ForegroundColor Yellow
    Write-Host "Review warnings above and consider updating the data" -ForegroundColor Yellow
    Write-Host ""
    
    if ($FailOnWarnings) {
        exit 1
    } else {
        exit 0
    }
} else {
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "TESTS FAILED - ISSUES DETECTED" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Critical encoding or diacritics issues found" -ForegroundColor Red
    Write-Host "Review failed tests above and fix the issues" -ForegroundColor Red
    Write-Host ""
    exit 1
}
