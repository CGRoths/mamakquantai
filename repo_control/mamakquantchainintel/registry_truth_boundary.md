# mamakquantchainintel — Registry Truth Boundary

> STATUS: provisional — pending MQAI-0001 verification.
> The canonical registry is a HIGH-risk area (per AGENTS.md consensus model).

## Principle

The ChainIntel canonical registry is the **single source of entity/label truth**. Its boundary is
governed: only the registry defines what an entity is and what it is labeled. Every other layer is a
consumer.

## Boundary rules (canonical intent)

1. **Single source.** No duplicate or shadow registries. Consumers read; they do not author.
2. **No cross-layer authorship.** MQNODE, MQENGINE, MQBOT never write registry truth.
3. **Governed mutations.** Adding, renaming, merging, or relabeling entities is a HIGH-risk,
   audited operation requiring full consensus + Cray approval.
4. **Referential integrity.** Downstream references to entity IDs must remain valid across changes;
   ID stability is a hard requirement.
5. **Provenance.** Every registry change records who/what/why and when.

## Enforcement

- `cross_layer_violation_check` blocks non-MQCHAIN writes to registry paths.
- Registry-touching changes → HIGH consensus mode.

## Open questions (for MQAI-0001)

- Exact registry storage location and schema within `mqchain-console`.
- How entity IDs are minted and referenced.
- Whether `mqchain-console` depends on parent-repo files (affects mapping scope).
