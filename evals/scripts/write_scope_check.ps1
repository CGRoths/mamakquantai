<#
.SYNOPSIS
  write_scope_check gate (V0). Post-run audit: assert all written paths stay in allowed job folders.
.DESCRIPTION
  Compares a supplied set of written paths against the allow-list globs from job.yaml.
  Fails if any path falls outside output/ (Codex) or review/ (Claude), or touches a product
  repo / repo_control/. V0 = post-run audit; V1 = FS-level prevention.
.NOTES
  STATUS: V0 stub. Wire actual write-set collection in the orchestrator.
#>
param(
  [Parameter(Mandatory = $true)] [string] $JobId,
  [string[]] $WrittenPaths = @(),
  [string]   $Root = "C:\MAMAKQUANT\mamakquantai"
)

$ErrorActionPreference = "Stop"

$jobDir       = Join-Path $Root "jobs\active\$JobId"
$allowOutput  = Join-Path $jobDir "output"
$allowReview  = Join-Path $jobDir "review"
$repoControl  = Join-Path $Root "repo_control"

$offending = @()
foreach ($p in $WrittenPaths) {
  $full = [System.IO.Path]::GetFullPath($p)
  $inScope = $full.StartsWith($allowOutput, 'OrdinalIgnoreCase') -or `
             $full.StartsWith($allowReview, 'OrdinalIgnoreCase')
  $touchesRepoControl = $full.StartsWith($repoControl, 'OrdinalIgnoreCase')
  if ((-not $inScope) -or $touchesRepoControl) { $offending += $full }
}

$status = if ($offending.Count -eq 0) { "pass" } else { "fail" }
$result = [ordered]@{
  gate            = "write_scope_check"
  status          = $status
  offending_paths = $offending
}
$result | ConvertTo-Json -Depth 5
if ($status -eq "fail") { exit 1 } else { exit 0 }
