# Validation record

Reviewed September 7, 2026. This record separates schema coverage, local validation, and live public observations.

## Official schema fingerprints

| Service | Schema version | Paths | Operations | SHA-256 |
| --- | --- | --- | --- | --- |
| [Goldsky management](https://api.goldsky.com/api/v1/docs/openapi.json) | `1.2.0` | 31 | 40 | `f6fad1c494df64a2b27edfcc67b41aa945031fa9a7fba3cc12fb0cbf037c5403` |

## Public observations

- Goldsky Edge public demo `eth_blockNumber` succeeded for Ethereum chain 1; observed block `25924854`. This is a connectivity check, not Polygon/Polymarket dataset verification.
- The public management OpenAPI document was retrieved successfully; schema version 1.2.0 contains 40 operations over 31 paths. No authenticated management request was executed.
- The community Uniswap GraphQL endpoint linked in Goldsky documentation returned HTTP 403 for a small `__typename` query. No successful GraphQL data/freshness claim is made.
- npm metadata reported `@goldskycom/cli` 13.10.2. It did not declare an engines minimum. The CLI and product extensions were not installed or executed.

## Local validation

Four unit tests passed: short REST pages with next cursors continue; repeated cursors and page-budget exhaustion fail; GraphQL partial-success errors are surfaced; backfill generation preserves required valid block bounds and rejects invalid ones.

YAML examples and the live configuration parse locally. README Python/shell/JSON blocks passed syntax checks. All internal contents anchors resolve. The generator emits valid JSON, also valid YAML, with an explicit finite block-number filter and job mode. This is local syntax/behavior validation, not Goldsky CLI or service acceptance.

## Limits

No Goldsky account, token, paid resource, pipeline, sink, webhook, or Compose app was created. No live Polymarket Turbo rows were inspected. Dataset field/semantics claims derive from official documentation. Exchange V3/PolyV2 contract coverage is explicitly unverified. No backfill completeness, production reorg handling, exactly-once effect, account quota, or cost estimate was experimentally validated.

## Repeatable maintenance

Rerun the included tests and public examples. Re-fetch the official schemas, compare operation/parameter coverage, and update fingerprints and review dates together. Validate deployment templates within your own project before executing them. Keep failed observations and incomplete coverage explicit. Record runtime and CLI/SDK versions; do not turn HTTP/GraphQL errors into empty datasets.
