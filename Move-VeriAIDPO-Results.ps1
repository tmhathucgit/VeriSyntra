# VeriAIDPO Results Auto-Move Script
# Purpose: Automatically move VeriAIDPO_Run_*.md files from Downloads to VeriSystems directory
# Usage: Run this script after downloading results from Google Colab

# Define source and destination paths
$DownloadsPath = "$env:USERPROFILE\Downloads"
$DestinationPath = "C:\Users\Administrator\OneDrive\Projects\GitHub\VeriSyntra\docs\VeriSystems"

# File pattern to match
$FilePattern = "VeriAIDPO_Run_*.md"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "VeriAIDPO Results Auto-Move Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Source:      $DownloadsPath" -ForegroundColor Yellow
Write-Host "Destination: $DestinationPath" -ForegroundColor Yellow
Write-Host "Pattern:     $FilePattern" -ForegroundColor Yellow
Write-Host ""

# Check if destination directory exists
if (-not (Test-Path $DestinationPath)) {
    Write-Host "ERROR: Destination directory does not exist!" -ForegroundColor Red
    Write-Host "Path: $DestinationPath" -ForegroundColor Red
    exit 1
}

# Find matching files in Downloads
$FilesToMove = Get-ChildItem -Path $DownloadsPath -Filter $FilePattern -ErrorAction SilentlyContinue

if ($FilesToMove.Count -eq 0) {
    Write-Host "No VeriAIDPO result files found in Downloads folder." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Looking for files matching: $FilePattern" -ForegroundColor Gray
    Write-Host "In: $DownloadsPath" -ForegroundColor Gray
    exit 0
}

# Move each file
Write-Host "Found $($FilesToMove.Count) file(s) to move:" -ForegroundColor Green
Write-Host ""

foreach ($File in $FilesToMove) {
    $DestinationFile = Join-Path -Path $DestinationPath -ChildPath $File.Name
    
    try {
        # Check if file already exists in destination
        if (Test-Path $DestinationFile) {
            $Overwrite = Read-Host "File '$($File.Name)' already exists. Overwrite? (y/n)"
            if ($Overwrite -ne 'y') {
                Write-Host "  SKIPPED: $($File.Name)" -ForegroundColor Yellow
                continue
            }
        }
        
        # Move the file
        Move-Item -Path $File.FullName -Destination $DestinationFile -Force
        Write-Host "  MOVED: $($File.Name)" -ForegroundColor Green
        Write-Host "    From: $($File.DirectoryName)" -ForegroundColor Gray
        Write-Host "    To:   $DestinationPath" -ForegroundColor Gray
        Write-Host ""
        
    } catch {
        Write-Host "  ERROR: Failed to move $($File.Name)" -ForegroundColor Red
        Write-Host "  Details: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host ""
    }
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Auto-move complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Open the moved file in VeriSystems directory" -ForegroundColor White
Write-Host "2. Review the results and analysis" -ForegroundColor White
Write-Host "3. Update VeriAIDPO_Training_Config_Tracking.md" -ForegroundColor White
Write-Host "4. Share results for Run 4 configuration (if needed)" -ForegroundColor White
