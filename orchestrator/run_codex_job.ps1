<#
.SYNOPSIS
  Run (semi-manual) a Codex build/map job through the MQAI control plane. V0.
.DESCRIPTION
  1. Loads the job.
  2. Packs and prints the Codex briefing (job spec + repo_control + skill guide references).
  3. (After Codex writes to output/) runs scripted eval gates and records eval_results.json.
  V0 is semi-manual: this wrapper prepares context and validates; it does not auto-drive Codex.
.PARAMETER JobId
  Job identifier, e.g. MQAI-0001.
.PARAMETER EvalsOnly
  Skip briefing; just run the scripted gates against current output/.
.NOTES
  STATUS: V0 stub. Does NOT touch product repos. Does NOT promote.
#>
param(
  [Parameter(Mandatory=$true)][string] $JobId,
  [switch] $EvalsOnly
)

$ErrorActionPreference = "Stop"
$root = "C:\MAMAKQUANT\mamakquantai"
. (Join-Path $root "orchestrator\lib\job_io.ps1")

$jobDir = Assert-JobExists $JobId
$yaml   = Read-JobYamlRaw $JobId

if (-not $EvalsOnly) {
  Write-Banner "MQAI Codex briefing: $JobId"
  Write-Output "Job spec: $jobDir\job.yaml"
  Write-Output ""
  Write-Output "--- job.yaml ---"
  Write-Output $yaml
  Write-Output ""
  Write-Output "Read before building:"
  Write-Output "  - AGENTS.md"
  Write-Output "  - company_brain/ (non_negotiables, separation_of_concerns)"
  Write-Output "  - skills/repo_mapper.md (for cartography jobs)"
  Write-Output "  - repo_control/<repo>/ for each target"
  Write-Output ""
  Write-Output "WRITE ONLY to: jobs/active/$JobId/output/"
  Write-Output "Product repos are READ-ONLY. Do not promote. Do not write repo_control/."
  Write-Output ""
  Write-Output "When Codex has written output/, re-run with -EvalsOnly to run gates."
  return
}

# --- Scripted eval gates (V0) ---
Write-Banner "Running scripted eval gates: $JobId"
$scripts   = Join-Path $root "evals\scripts"
$reviewDir = Join-Path $jobDir "review"
if (-not (Test-Path $reviewDir)) { New-Item -ItemType Directory -Path $reviewDir | Out-Null }

# NOTE: TouchedPaths / WrittenPaths collection is wired by the orchestrator in a later iteration.
# V0: pass empty sets; read-only mapping jobs have no product-repo writes.
$results = @()
$results += (& (Join-Path $scripts "risk_tier_assignment.ps1") -JobId $JobId -Repos @("mqnode_test2","mqnode_cloud","mqengine","mamakquantchainintel") | ConvertFrom-Json)
$results += (& (Join-Path $scripts "write_scope_check.ps1")     -JobId $JobId | ConvertFrom-Json)
$results += (& (Join-Path $scripts "secret_scan.ps1")           -JobId $JobId | ConvertFrom-Json)

$outFile = Join-Path $reviewDir "eval_results.json"
$results | ConvertTo-Json -Depth 6 | Out-File -FilePath $outFile -Encoding utf8
Write-Output "Wrote $outFile"
Write-Output "Checklist gates (cross_layer/formula/migration/lookahead) are executed by Claude in review."
