<#
.SYNOPSIS
  secret_scan gate (V0). Regex/entropy scan of staged output for secrets.
.DESCRIPTION
  Scans jobs/active/<JobId>/output/ for common secret patterns. Logs file + pattern name only,
  never the secret value. Any hit = fail. V1 = gitleaks/trufflehog.
.NOTES
  STATUS: V0 stub. Patterns are a starting set; extend as needed.
#>
param(
  [Parameter(Mandatory = $true)] [string] $JobId,
  [string] $Root = "C:\MAMAKQUANT\mamakquantai"
)

$ErrorActionPreference = "Stop"

$outputDir = Join-Path $Root "jobs\active\$JobId\output"

$patterns = @(
  @{ name = "private_key_block"; regex = "-----BEGIN [A-Z ]*PRIVATE KEY-----" },
  @{ name = "aws_access_key";    regex = "AKIA[0-9A-Z]{16}" },
  @{ name = "bearer_token";      regex = "(?i)bearer\s+[A-Za-z0-9\-_\.=]{20,}" },
  @{ name = "generic_api_key";   regex = "(?i)(api[_-]?key|secret|token)\s*[:=]\s*['""]?[A-Za-z0-9\-_]{16,}" },
  @{ name = "dotenv_assignment"; regex = "(?m)^[A-Z0-9_]{3,}=[^\s]{8,}$" }
)

$hits = @()
if (Test-Path $outputDir) {
  $files = Get-ChildItem -Path $outputDir -Recurse -File -ErrorAction SilentlyContinue
  foreach ($f in $files) {
    $content = Get-Content -Path $f.FullName -Raw -ErrorAction SilentlyContinue
    if ($null -eq $content) { continue }
    foreach ($p in $patterns) {
      if ([regex]::IsMatch($content, $p.regex)) {
        $hits += [ordered]@{ file = $f.FullName; pattern = $p.name }
      }
    }
  }
}

$status = if ($hits.Count -eq 0) { "pass" } else { "fail" }
$result = [ordered]@{ gate = "secret_scan"; status = $status; hits = $hits }
$result | ConvertTo-Json -Depth 5
if ($status -eq "fail") { exit 1 } else { exit 0 }
