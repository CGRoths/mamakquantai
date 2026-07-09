# Hard-Stop Policy (global)

MQAI stops immediately and reports (stop reason · files inspected · files changed · safest next
action) if any of the following would occur:

- push to a remote
- git history rewrite
- inspecting or printing secret contents
- modifying a product repo (unless the active job explicitly authorizes it)
- deleting a pre-existing user/product/secret file
- overwriting an existing MQAI active job
- git state too ambiguous to proceed safely
- tests failing in a way that could corrupt MQAI job history
- modifying any path outside C:/MAMAKQUANT/mamakquantai
- generated code requiring an uninstalled dependency that cannot degrade gracefully

Global forbidden actions (never, without an explicit approved job authorizing them):
- modify trading formulas, live execution code, schema/migrations, or MQCHAIN registry truth
- `git add -A` in product repos
- silently promote agent output into canonical `repo_control/` truth
- bypass Cray approval for high-risk gates
- claim Claude/Codex/OpenRouter are wired when they are not
