<#
.SYNOPSIS
  risk_tier_assignment gate (V0). Path-matched risk tiering. Runs FIRST.
.DESCRIPTION
  Matches touched paths against repo_control/<repo>/critical_files.md globs. Any match => HIGH.
  A repo without critical_files.md => default HIGH (conservative). Tier is path-derived,
  NEVER agent self-assessment. Ambiguous/unmapped => HIGH.
.NOTES
  STATUS: V0 stub. TouchedPaths supplied by orchestrator; for read-only jobs may be empty.
#>
param(
  [Parameter(Mandatory = $true)] [string]   $JobId,
  [Parameter(Mandatory = $true)] [string[]] $Repos,
  [string[]] $TouchedPaths = @(),
  [string]   $Root = "C:\MAMAKQUANT\mamakquantai"
)

$ErrorActionPreference = "Stop"

function Convert-GlobToRegex([string] $glob) {
  $esc = [regex]::Escape($glob)
  $esc = $esc.Replace('\*\*', '.*').Replace('\*', '[^/\\]*').Replace('\?', '.')
  return "^$esc$"
}

$matched = @()
$tier    = "LOW"

foreach ($repo in $Repos) {
  $cfPath = Join-Path $Root "repo_control\$repo\critical_files.md"
  if (-not (Test-Path $cfPath)) {
    # No critical_files.md => conservative default.
    $tier = "HIGH"
    $matched += "$repo::(no critical_files.md -> default HIGH)"
    continue
  }

  # Extract glob lines from fenced code blocks in critical_files.md.
  $globs = Get-Content $cfPath |
           Where-Object { $_ -match '^\s*(\*\*|[\w./\-*?]+)\s*(#.*)?$' -and $_ -notmatch '^\s*#' } |
           ForEach-Object { ($_ -replace '#.*$', '').Trim() } |
           Where-Object { $_ -ne '' }

  if ($globs -contains '**') { $tier = "HIGH"; $matched += "$repo::**"; continue }

  foreach ($tp in $TouchedPaths) {
    foreach ($g in $globs) {
      if ($tp -match (Convert-GlobToRegex $g)) { $tier = "HIGH"; $matched += "$repo::$g -> $tp" }
    }
  }
}

$result = [ordered]@{
  gate    = "risk_tier_assignment"
  status  = "pass"
  tier    = $tier
  matched = $matched
}
$result | ConvertTo-Json -Depth 5
exit 0
