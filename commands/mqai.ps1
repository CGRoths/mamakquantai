<#
.SYNOPSIS
  MQAI local control-plane CLI wrapper (V1). Thin shim over orchestrator/mqai_runner.py.

.EXAMPLE
  .\commands\mqai.ps1 status  MQAI-0005
  .\commands\mqai.ps1 next    MQAI-0005
  .\commands\mqai.ps1 context MQAI-0005
  .\commands\mqai.ps1 report  MQAI-0005
  .\commands\mqai.ps1 prompts MQAI-0005
  .\commands\mqai.ps1 eval    MQAI-0005
  .\commands\mqai.ps1 run     MQAI-0005 --until-hard-stop
  .\commands\mqai.ps1 approve MQAI-0005 --gate plan
  .\commands\mqai.ps1 approve MQAI-0005 --gate execution
  .\commands\mqai.ps1 approve MQAI-0005 --gate final_commit
  .\commands\mqai.ps1 handoff MQAI-0005 --from codex --to claude --stop-reason context_exhausted
  .\commands\mqai.ps1 handoff MQAI-0005 --from claude --to codex
  .\commands\mqai.ps1 resume  MQAI-0005 --agent claude
  .\commands\mqai.ps1 resume  MQAI-0005 --agent codex
  .\commands\mqai.ps1 resume  MQAI-0005 --agent gpt

.NOTES
  Read-only / dry-run by default. No push, no history rewrite, no product-repo writes.
  If PowerShell execution policy blocks this script, run the underlying python directly:
    python orchestrator/mqai_runner.py <command> <job_id> [args]
#>
param(
  [Parameter(Mandatory = $true, Position = 0)] [string] $Command,
  [Parameter(Mandatory = $false, Position = 1)] [string] $JobId,
  [Parameter(ValueFromRemainingArguments = $true)] [string[]] $Rest
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot   # repo root (commands/ is one level down)
$runner = Join-Path $root "orchestrator\mqai_runner.py"

if (-not (Test-Path $runner)) {
  Write-Error "runner not found: $runner"
  exit 3
}

# Resolve a python interpreter.
$py = $null
foreach ($cand in @("python", "py", "python3")) {
  $cmd = Get-Command $cand -ErrorAction SilentlyContinue
  if ($cmd) { $py = $cand; break }
}
if (-not $py) {
  Write-Error "Python not found on PATH. Install Python 3, or run the runner manually."
  exit 3
}

$argList = @($runner, $Command)
if ($JobId) { $argList += $JobId }
if ($Rest)  { $argList += $Rest }

Push-Location $root
try {
  & $py @argList
  exit $LASTEXITCODE
}
finally {
  Pop-Location
}
