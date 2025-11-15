# run_and_test.ps1
# Starts the Flask app using the venv Python in this project,
# waits until the server responds, runs a few test requests and prints results.
# Usage: Open PowerShell, navigate to project and run:
#   powershell -ExecutionPolicy Bypass -File .\run_and_test.ps1

Set-StrictMode -Version Latest
$project = 'C:\estoque_app'
$python = Join-Path $project 'venv\Scripts\python.exe'
if (-not (Test-Path $python)) {
  Write-Error "Python venv not found at $python. Activate your venv or adjust the path."
  exit 1
}

Set-Location $project

# Start Flask as a background job
$job = Start-Job -ScriptBlock {
  param($py, $proj)
  & $py "$proj\app.py"
} -ArgumentList $python, $project
Write-Host "Started Flask server as job Id $($job.Id). Waiting for server to respond..."

$baseUrl = 'http://127.0.0.1:5000'
$maxWait = 30
$elapsed = 0
$serverUp = $false
while ($elapsed -lt $maxWait) {
  try {
    $r = Invoke-WebRequest -Uri $baseUrl -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
    Write-Host "Server is up (HTTP $($r.StatusCode))"
    $serverUp = $true
    break
  } catch {
    Start-Sleep -Seconds 1
    $elapsed += 1
  }
}

if (-not $serverUp) {
  Write-Host "Server did not start within $maxWait seconds. Showing server job output (if any):"
  Receive-Job -Id $job.Id -Keep | Select-Object -First 200 | ForEach-Object { Write-Host $_ }
  Stop-Job -Id $job.Id -Force
  Remove-Job -Id $job.Id
  exit 1
}

Function Test-EndPoint($path, $method = 'GET', $body = $null) {
  $uri = "$baseUrl$path"
  Write-Host "\n=> $method $uri"
  try {
    if ($method -eq 'GET') {
      $res = Invoke-RestMethod -Uri $uri -Method GET -TimeoutSec 10 -ErrorAction Stop
      Write-Host (ConvertTo-Json $res -Depth 6)
    } elseif ($method -eq 'POST') {
      $res = Invoke-RestMethod -Uri $uri -Method POST -Body ($body | ConvertTo-Json) -ContentType 'application/json' -TimeoutSec 10 -ErrorAction Stop
      Write-Host (ConvertTo-Json $res -Depth 6)
    }
  } catch {
    Write-Host "ERROR: $($_.Exception.Message)"
  }
}

# Run tests
Test-EndPoint '/init'
Test-EndPoint '/estoque'
Test-EndPoint '/'

# Example POST tests (uncomment to run)
#Test-EndPoint '/entrada' 'POST' @{ material_id = 1; quantidade = 5 }
#Test-EndPoint '/saida'  'POST' @{ material_id = 1; quantidade = 2 }

Write-Host "\nStopping server job..."
Stop-Job -Id $job.Id -Force
Remove-Job -Id $job.Id
Write-Host "Done."