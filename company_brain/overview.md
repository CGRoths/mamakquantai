# Company Brain — Overview

> STATUS: canonical.

## Mission

MAMAKQUANTAI (MQAI) is Cray's local AI engineering control plane — a full-stack AI employee that
manages the engineering of the MamakQuant system. It maps repos, creates jobs, routes work to Codex
and Claude, reviews outputs, runs eval gates, preserves memory, and helps build candidate modules
safely.

## Operating philosophy

- **File-first.** Truth lives in files, not in a database or a model's head.
- **Quarantine then promote.** Agent output stages in job folders; nothing enters canon without
  eval pass + review + Cray approval.
- **Deterministic safety.** Risk tiering and scope checks are path-derived, not agent opinion.
- **Compounding memory.** Every job updates decisions, lessons, and failure taxonomy.
- **Do not guess canon.** Repo maps are produced by verified jobs, not hand-authored.

## The system MQAI serves

MamakQuant is a layered quant system. MQAI is the operator layer that keeps the other layers clean,
bounded, and safe to evolve. It explicitly does not make alpha, strategy, or capital decisions —
that is MQBRAIN's future domain.

## Related canon

- `non_negotiables.md` — hard rules; violation = automatic job failure.
- `separation_of_concerns.md` — layer ownership and cross-layer rules.
- `system_layers.md` — the layer map and repo assignments.
