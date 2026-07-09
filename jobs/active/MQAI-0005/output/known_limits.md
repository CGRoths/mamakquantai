# MQAI-0005 — Known Limits (job copy)

Canonical list: `docs/known_limits.md`. Summary for this job:

- No agent APIs wired (Claude/Codex/OpenRouter) — prompts are files for manual/CLI use.
- State inference is a filename/artifact heuristic; under-claims by design.
- `close` is dry-run only; real closeout is a governed manual step.
- `approve` writes an `approved_<gate>.md` artifact; it does not auto-flip execution/commit/push
  flags in job.yaml (avoids unsafe YAML rewrites).
- `minimal_yaml` is a subset parser (PyYAML used if present).
- `eval_runner` uses Python-native gates; `git_status_capture`/`touched_path_check` return honest
  `skipped` without product inputs. The `.ps1` gate scripts are an alternative surface.
- Control plane never pushes / rewrites history / inspects secrets / writes product repos.
