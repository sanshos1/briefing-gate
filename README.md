# BriefingGate

> Turn two independent public notices into one attributable operational briefing.

BriefingGate is a GenLayer Intelligent Contract for the moment between "we have received reports" and "we are ready to publish an operational brief." It does not ask a single operator to summarize the situation. Instead, it requires validators to independently retrieve two records, agree on a concise situation summary and actionable steps, then preserve the evidence digests behind the published result.

## Why this exists

Operational teams often receive fragmented notices from different publishers: an incident bulletin, a regulator update, an outage report, or a safety notice. A useful brief needs to be concise, but it must not silently turn one unverified report into an instruction.

BriefingGate creates a reusable gate:

1. Collect two notices hosted by different HTTPS origins.
2. Ask GenLayer validators to retrieve both notices independently.
3. Produce a bounded summary and one to four actions only when both records support them.
4. Store the source digests and move the brief to `SYNTHESIZED`.
5. Let the owner publish the reviewed brief, or archive it if it should not proceed.

## Contract lifecycle

```text
COLLECTING
  |  synthesize_briefing()
  v
SYNTHESIZED
  |  publish_briefing() by owner       archive_briefing() by owner
  v                                  v
PUBLISHED                          ARCHIVED
```

The contract has no hidden "approved" shortcut. A brief cannot be published directly from collection, and an archived brief cannot be republished.

## Public methods

| Method | Who can call it | Purpose |
| --- | --- | --- |
| `collect_briefing` | Anyone | Registers an audience and two differently hosted notices. |
| `synthesize_briefing` | Anyone | Runs validator consensus and records summary, actions, and digests. |
| `publish_briefing` | Brief owner | Publishes a synthesized brief. |
| `archive_briefing` | Brief owner | Stops an unfinished brief. |
| `get_briefing` | Anyone | Reads the evidence-backed state. |

## What validators agree on

The contract does not accept a leader result just because it is valid JSON. Every validator re-fetches the notices and recomputes the fields that affect stored state:

- the short situation summary;
- the ordered operational actions;
- the SHA-256 digest for each retrieved record.

For a result to be stored, the leader's summary, actions, and digests must match the validator's independently computed result. Both notice indexes must be present; one source alone cannot support a published briefing.

## Safety boundaries

- Duplicate briefing IDs are rejected after normalization.
- Notice URLs must be normalized HTTPS URLs, with no credentials embedded.
- The two notice hosts must differ.
- Unavailable or non-200 sources stop synthesis rather than yielding invented output.
- Summaries and actions are length-bounded before storage.
- Only the original owner can publish or archive a brief.
- Fetched web content is treated as untrusted data, never as instructions.

Different URLs are not automatically independent authorities. Deployers should choose sources with genuinely separate editorial or institutional control and should label any operator-created records as demo fixtures.

## Quick start

```python
contract.collect_briefing(
    "OPS-2026-001",
    "Regional operations team",
    "https://publisher-a.example/notices/incident-17",
    "https://publisher-b.example/advisories/incident-17",
)

contract.synthesize_briefing("OPS-2026-001")
contract.publish_briefing("OPS-2026-001")
```

Use `get_briefing("OPS-2026-001")` to retrieve the stored summary, actions, original URLs, and digests.

## Local verification

```bash
PYTHONUTF8=1 genvm-lint contracts/contract.py
python -m pytest -q
```

## Deployment

| Network | Contract |
| --- | --- |
| StudioNet | [`0x1FDeC0FfF41D0ed0d291b6372cDD9ba5e42fa005`](https://explorer-studio.genlayer.com/address/0x1FDeC0FfF41D0ed0d291b6372cDD9ba5e42fa005) |

The deployment transaction and the account-specific deployment record are available in [`deployment.json`](deployment.json).
