<#
.SYNOPSIS
    Safe PostgreSQL migration runner with Vietnamese UTF-8 encoding protection
    
.DESCRIPTION
    Executes SQL migration files against PostgreSQL Docker container while
    preserving Vietnamese UTF-8 diacritics. Includes automatic encoding verification.
    
    VeriSyntra Standard: ALWAYS use this script for migrations with Vietnamese text.
    DO NOT use: Get-Content | docker exec (corrupts UTF-8)
    
.PARAMETER MigrationFile
    Path to SQL migration file (relative or absolute)
    
.PARAMETER Container
    Docker container name (default: verisyntra-postgres)
    
.PARAMETER Database
    Database name (default: verisyntra)
    
.PARAMETER User
    Database user (default: verisyntra)
    
.PARAMETER VerifyEncoding
    Enable Vietnamese UTF-8 encoding verification (default: $true)
    
.PARAMETER CleanupTemp
    Remove temporary file from container after execution (default: $true)
    
.EXAMPLE
    .\run_migration_safe.ps1 -MigrationFile "backend\veri_ai_data_inventory\migrations\add_permissions_table.sql"
    
.EXAMPLE
    .\run_migration_safe.ps1 -MigrationFile "migrations\step2.sql" -VerifyEncoding $true
    
.NOTES
    Author: VeriSyntra Team
    Date: November 8, 2025
    Purpose: Prevent Vietnamese UTF-8 encoding corruption in database migrations
#>

param(
    [Parameter(Mandatory=$true, HelpMessage="Path to SQL migration file")]
    [string]$MigrationFile,
    
    [Parameter(Mandatory=$false)]
    [string]$Container = "verisyntra-postgres",
    
    [Parameter(Mandatory=$false)]
    [string]$Database = "verisyntra",
    
    [Parameter(Mandatory=$false)]
    [string]$User = "verisyntra",
    
    [Parameter(Mandatory=$false)]
    [bool]$VerifyEncoding = $true,
    
    [Parameter(Mandatory=$false)]
    [bool]$CleanupTemp = $true
)

# Color output functions
function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Failure {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Validation functions
function Test-DockerContainer {
    param([string]$ContainerName)
    
    $containerRunning = docker ps --filter "name=$ContainerName" --format "{{.Names}}" 2>$null
    
    if ($containerRunning -eq $ContainerName) {
        return $true
    }
    
    return $false
}

function Test-VietnameseEncoding {
    param(
        [string]$ContainerName,
        [string]$DatabaseName,
        [string]$UserName
    )
    
    Write-Info "Verifying Vietnamese UTF-8 encoding..."
    
    # First check if permissions table exists and has data
    $checkTable = @"
SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_name = 'permissions'
);
"@
    
    $tableExists = docker exec $ContainerName psql -U $UserName -d $DatabaseName -t -c $checkTable 2>$null
    
    if ($tableExists -notmatch 't') {
        Write-Info "Permissions table not found - skipping encoding verification"
        return $null
    }
    
    # Query to check if Vietnamese diacritics are properly stored
    $query = @"
SELECT 
    COUNT(*) FILTER (WHERE octet_length(permission_name_vi) > length(permission_name_vi)) as utf8_correct,
    COUNT(*) FILTER (WHERE octet_length(permission_name_vi) = length(permission_name_vi)) as possibly_corrupted,
    COUNT(*) as total
FROM permissions
WHERE permission_name_vi IS NOT NULL AND permission_name_vi != '';
"@
    
    $result = docker exec $ContainerName psql -U $UserName -d $DatabaseName -t -c $query 2>$null
    
    if ($LASTEXITCODE -eq 0 -and $result) {
        $parts = $result.Trim() -split '\|'
        
        if ($parts.Count -eq 3) {
            $utf8Correct = [int]$parts[0].Trim()
            $corrupted = [int]$parts[1].Trim()
            $total = [int]$parts[2].Trim()
            
            if ($total -eq 0) {
                Write-Info "No Vietnamese data found in permissions table yet"
                return $null
            }
            
            Write-Info "Encoding verification results:"
            Write-Host "  - UTF-8 Vietnamese: $utf8Correct records" -ForegroundColor Cyan
            Write-Host "  - Possibly corrupted: $corrupted records" -ForegroundColor $(if ($corrupted -gt 0) { "Yellow" } else { "Cyan" })
            Write-Host "  - Total: $total records" -ForegroundColor Cyan
            
            if ($corrupted -gt 0) {
                Write-Warning "Some records may have encoding issues (char_count = byte_count)"
                Write-Warning "This might indicate ASCII corruption of Vietnamese diacritics"
                return $false
            }
            
            if ($utf8Correct -gt 0) {
                Write-Success "Vietnamese UTF-8 encoding verified (byte_count > char_count)"
                return $true
            }
        }
    }
    
    Write-Info "Could not verify encoding - table may be empty"
    return $null
}

# Main execution
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VeriSyntra Safe Migration Runner" -ForegroundColor Cyan
Write-Host "Vietnamese UTF-8 Encoding Protection" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Validate migration file exists
Write-Info "Step 1: Validating migration file..."

if (-not (Test-Path $MigrationFile)) {
    Write-Failure "Migration file not found: $MigrationFile"
    exit 1
}

$migrationFileInfo = Get-Item $MigrationFile
Write-Success "Found migration file: $($migrationFileInfo.Name) ($($migrationFileInfo.Length) bytes)"

# Check file encoding and Vietnamese diacritics
$encoding = $null
$hasDiacriticIssues = $false
try {
    $content = Get-Content $MigrationFile -Encoding UTF8 -Raw
    
    # Check for Vietnamese diacritics using Unicode ranges
    if ($content -match '[\u1EA0-\u1EF9]') {
        Write-Success "Vietnamese diacritics detected in file"
        $encoding = "UTF-8 with Vietnamese"
    } else {
        $encoding = "UTF-8"
    }
    
    # Check for common Vietnamese words WITHOUT diacritics (potential issues)
    $suspiciousPatterns = @(
        "nguoi\s+dung",      # Should be: người dùng
        "cong\s+ty",          # Should be: công ty
        "dia\s+chi",          # Should be: địa chỉ
        "quan\s+ly",          # Should be: quản lý
        "bao\s+mat",          # Should be: bảo mật
        "nhan\s+vien",        # Should be: nhân viên
        "chu\s+the",          # Should be: chủ thể
        "du\s+lieu",          # Should be: dữ liệu
        "hop\s+dong",         # Should be: hợp đồng
        "phap\s+luat",        # Should be: pháp luật
        "dang\s+ky",          # Should be: đăng ký
        "thong\s+tin",        # Should be: thông tin
        "'nguoi dung'",       # In quotes
        "'cong ty'",
        "'quan ly'",
        "'bao mat'"
    )
    
    foreach ($pattern in $suspiciousPatterns) {
        if ($content -match $pattern) {
            $hasDiacriticIssues = $true
            Write-Warning "Possible Vietnamese without diacritics detected: '$($matches[0])'"
        }
    }
    
    if ($hasDiacriticIssues) {
        Write-Host ""
        Write-Warning "Migration file may contain Vietnamese text without proper diacritics"
        Write-Info "Common corrections needed:"
        Write-Host "  - 'nguoi dung' -> 'người dùng'" -ForegroundColor Yellow
        Write-Host "  - 'cong ty' -> 'công ty'" -ForegroundColor Yellow
        Write-Host "  - 'dia chi' -> 'địa chỉ'" -ForegroundColor Yellow
        Write-Host "  - 'quan ly' -> 'quản lý'" -ForegroundColor Yellow
        Write-Host "  - 'bao mat' -> 'bảo mật'" -ForegroundColor Yellow
        Write-Host ""
        
        $response = Read-Host "Continue anyway? (y/N)"
        if ($response -ne 'y' -and $response -ne 'Y') {
            Write-Info "Migration cancelled. Please fix Vietnamese diacritics and try again."
            exit 1
        }
    }
    
} catch {
    Write-Warning "Could not verify file encoding"
}

# Step 2: Validate Docker container
Write-Info "Step 2: Checking Docker container..."

if (-not (Test-DockerContainer -ContainerName $Container)) {
    Write-Failure "Docker container '$Container' is not running"
    Write-Info "Start the container with: docker-compose up -d postgres"
    exit 1
}

Write-Success "Container '$Container' is running"

# Step 3: Test database connection
Write-Info "Step 3: Testing database connection..."

docker exec $Container psql -U $User -d $Database -c "SELECT 1;" 2>$null | Out-Null

if ($LASTEXITCODE -ne 0) {
    Write-Failure "Cannot connect to database '$Database' as user '$User'"
    exit 1
}

Write-Success "Database connection successful"

# Step 4: Copy migration file to container (preserves UTF-8)
Write-Info "Step 4: Copying migration file to container..."

$tempFile = "/tmp/migration_$((Get-Date -Format 'yyyyMMdd_HHmmss')).sql"

docker cp $MigrationFile "${Container}:${tempFile}" 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Failure "Failed to copy migration file to container"
    exit 1
}

Write-Success "Migration file copied to container: $tempFile"

# Step 5: Execute migration
Write-Info "Step 5: Executing migration..."
Write-Host ""

$migrationOutput = docker exec $Container psql -U $User -d $Database -f $tempFile 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Failure "Migration execution failed"
    Write-Host $migrationOutput -ForegroundColor Red
    
    if ($CleanupTemp) {
        docker exec $Container rm $tempFile 2>$null
    }
    
    exit 1
}

Write-Host $migrationOutput
Write-Host ""
Write-Success "Migration executed successfully"

# Step 6: Verify Vietnamese encoding (if enabled)
if ($VerifyEncoding) {
    Write-Host ""
    $encodingOk = Test-VietnameseEncoding -ContainerName $Container -DatabaseName $Database -UserName $User
    
    if ($encodingOk -eq $false) {
        Write-Warning "Encoding verification detected potential issues"
        Write-Info "Run this query to investigate:"
        $investigateQuery = "SELECT permission_name, length(permission_name_vi), octet_length(permission_name_vi) FROM permissions LIMIT 5;"
        Write-Host "  docker exec $Container psql -U $User -d $Database -c `"$investigateQuery`"" -ForegroundColor Yellow
    }
}

# Step 7: Cleanup temporary file
if ($CleanupTemp) {
    Write-Info "Step 7: Cleaning up temporary file..."
    docker exec $Container rm $tempFile 2>$null
    Write-Success "Temporary file removed from container"
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Migration Complete" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Success "File: $($migrationFileInfo.Name)"
Write-Success "Container: $Container"
Write-Success "Database: $Database"
if ($encoding) {
    Write-Success "Encoding: $encoding"
}
Write-Host ""
Write-Info "Next steps:"
Write-Host "  1. Review migration output above"
Write-Host "  2. Test your application with the new schema"
Write-Host "  3. Update documentation if needed"
Write-Host ""

exit 0
