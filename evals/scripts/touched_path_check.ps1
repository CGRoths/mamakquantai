<#
.SYNOPSIS
  touched_path_check gate. Assert staged/touched paths in a product repo are a subset of the job's
  allowed_writes. Read-only (uses git metadata only; no content, no unrestricted diff).
.NOTES
  V1: the Python-native eval_runner is the primary surface. This script is an alternative for
  product-repo execution jobs. Emits JSON. Marks 'skipped' (never fake pass) if inputs are absent.
#>
param(
  [Parameter(Mandatory = $true)] [string] $RepoPath,
  [Parameter(Mandatory = $true)] [string[]] $AllowedGlobs
)
$ErrorActionPreference = "Stop"

if (-not (Test-Path (Join-Path $RepoPath ".git"))) {
  [ordered]@{ gate = "touched_path_check"; status = "skipped"; reason = "not a git repo: $RepoPath" } | ConvertTo-Json
  exit 0
}

# name-only staged paths (metadata only; NO content, NO unrestricted diff)
$touched = & git -C $RepoPath diff --cached --name-only
if (-not $touched) {
  [ordered]@{ gate = "touched_path_check"; status = "skipped"; reason = "no staged paths" } | ConvertTo-Json
  exit 0
}

$offending = @()
foreach ($p in $touched) {
  $inScope = $false
  foreach ($g in $AllowedGlobs) {
    $regex = "^" + [Regex]::Escape($g).Replace("\*\*", ".*").Replace("\*", "[^/]*") + "$"
    if ($p -match $regex) { $inScope = $true; break }
  }
  if (-not $inScope) { $offending += $p }
}

$status = if ($offending.Count -eq 0) { "pass" } else { "fail" }
[ordered]@{ gate = "touched_path_check"; status = $status; offending = $offending } | ConvertTo-Json -Depth 4
if ($status -eq "fail") { exit 1 } else { exit 0 }
