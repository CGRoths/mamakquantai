<#
.SYNOPSIS
  Shared orchestrator helpers (V0): job path resolution, job.yaml loading, path-guard.
.NOTES
  STATUS: V0 stub. Dot-source this from run_codex_job.ps1 / run_claude_review.ps1.
  YAML parsing is intentionally minimal in V0 (no external modules).
#>

$script:MqaiRoot = "C:\MAMAKQUANT\mamakquantai"

function Get-JobDir {
  param([Parameter(Mandatory=$true)][string] $JobId)
  return (Join-Path $script:MqaiRoot "jobs\active\$JobId")
}

function Assert-JobExists {
  param([Parameter(Mandatory=$true)][string] $JobId)
  $dir = Get-JobDir $JobId
  if (-not (Test-Path (Join-Path $dir "job.yaml"))) {
    throw "Job $JobId not found at $dir (expected job.yaml)."
  }
  return $dir
}

function Read-JobYamlRaw {
  # V0: return raw text; callers grep for the fields they need.
  param([Parameter(Mandatory=$true)][string] $JobId)
  $dir = Assert-JobExists $JobId
  return (Get-Content (Join-Path $dir "job.yaml") -Raw)
}

function Test-PathInScope {
  # Guard: is $Path inside $AllowedRoot?
  param(
    [Parameter(Mandatory=$true)][string] $Path,
    [Parameter(Mandatory=$true)][string] $AllowedRoot
  )
  $full = [System.IO.Path]::GetFullPath($Path)
  return $full.StartsWith([System.IO.Path]::GetFullPath($AllowedRoot), 'OrdinalIgnoreCase')
}

function Write-Banner {
  param([string] $Text)
  Write-Output ("=" * 72)
  Write-Output $Text
  Write-Output ("=" * 72)
}
