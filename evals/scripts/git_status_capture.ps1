<#
.SYNOPSIS
  git_status_capture gate. Capture read-only git metadata (branch, HEAD, porcelain status) for a
  target repo into an evidence file. No content, no unrestricted diff, no mutation.
.NOTES
  V1 alternative surface for product-repo execution jobs. Emits JSON summary; writes capture file.
#>
param(
  [Parameter(Mandatory = $true)] [string] $RepoPath,
  [Parameter(Mandatory = $true)] [string] $OutFile
)
$ErrorActionPreference = "Stop"

if (-not (Test-Path (Join-Path $RepoPath ".git"))) {
  [ordered]@{ gate = "git_status_capture"; status = "skipped"; reason = "not a git repo: $RepoPath" } | ConvertTo-Json
  exit 0
}

$branch = & git -C $RepoPath rev-parse --abbrev-ref HEAD
$head   = & git -C $RepoPath rev-parse --short HEAD
$porc   = & git -C $RepoPath status --porcelain

$lines = @("# repo: $RepoPath", "# branch: $branch", "# head: $head", "# --- status --porcelain ---") + $porc
$dir = Split-Path -Parent $OutFile
if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir | Out-Null }
$lines | Out-File -FilePath $OutFile -Encoding utf8

[ordered]@{
  gate = "git_status_capture"; status = "pass"; branch = $branch; head = $head;
  dirty_count = ($porc | Measure-Object).Count; out_file = $OutFile
} | ConvertTo-Json -Depth 4
exit 0
