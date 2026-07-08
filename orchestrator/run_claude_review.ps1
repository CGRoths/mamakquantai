<#
.SYNOPSIS
  Prepare (semi-manual) a Claude review for a job. V0.
.DESCRIPTION
  1. Verifies output/ exists and eval_results.json is present.
  2. Prints the review briefing (what to read, verdict block format).
  3. Reminds that Claude writes ONLY to review/ and cannot promote.
  V0 is semi-manual: this wrapper prepares context; it does not auto-drive Claude.
.PARAMETER JobId
  Job identifier, e.g. MQAI-0001.
.NOTES
  STATUS: V0 stub. Does NOT promote.
#>
param(
  [Parameter(Mandatory=$true)][string] $JobId
)

$ErrorActionPreference = "Stop"
$root = "C:\MAMAKQUANT\mamakquantai"
. (Join-Path $root "orchestrator\lib\job_io.ps1")

$jobDir    = Assert-JobExists $JobId
$outputDir = Join-Path $jobDir "output"
$reviewDir = Join-Path $jobDir "review"
$evalFile  = Join-Path $reviewDir "eval_results.json"

Write-Banner "MQAI Claude review briefing: $JobId"

if (-not (Test-Path $outputDir)) { throw "No output/ found for $JobId. Run Codex job first." }
if (-not (Test-Path $evalFile))  { Write-Output "WARNING: eval_results.json not found. Run gates (-EvalsOnly) first." }

Write-Output "Review target: $outputDir"
Write-Output "Eval results : $evalFile"
Write-Output ""
Write-Output "Read before reviewing:"
Write-Output "  - skills/code_reviewer.md"
Write-Output "  - relevant skills/*_guard.md for each target layer"
Write-Output "  - repo_control/<repo>/rules.md"
Write-Output ""
Write-Output "Execute checklist gates: cross_layer_violation, formula_diff, migration_required, lookahead_safety."
Write-Output ""
Write-Output "WRITE ONLY to: jobs/active/$JobId/review/  (do NOT promote, do NOT edit output/)"
Write-Output ""
Write-Output "Write review/claude_review.md with verdict block:"
Write-Output "  VERDICT: approve | request_changes | reject"
Write-Output "  FINDINGS: [ ... ]"
Write-Output "  BOUNDARY_CHECK: pass | fail"
Write-Output "  PROMOTE_RECOMMENDATION: yes | no"
Write-Output ""
Write-Output "After review, Cray records the decision in review/cray_decision.md (DECISION: approve|reject)."
