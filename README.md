# Goldsky Polymarket Guide: Turbo V2 Datasets, APIs, Subgraphs & Indexing

Use **Goldsky for Polymarket onchain data** with current Turbo datasets, bounded historical backfills, PostgreSQL or webhook sinks, and explicit data-quality checks. This independent developer guide also explains Goldsky REST management APIs, GraphQL subgraphs, Mirror, Edge RPC, Compose, CLI tooling, authentication, pagination, and operational limits.

**Critical migration fact:** Goldsky's official Polymarket page says Polymarket stopped using subgraphs going forward after its April 28, 2026 contract migration. Existing public Polymarket subgraphs can return incomplete or incorrect data. The documented current path is **Turbo Pipelines with V2 Polymarket datasets**. An old endpoint returning HTTP 200 is not proof of current coverage. [Official Polymarket indexing notice](https://docs.goldsky.com/chains/polymarket)

**Maintainer:** [geenes](https://github.com/geenes) · **Reviewed:** September 7, 2026 · **Scope:** Polymarket-focused indexing, plus the Goldsky platform interfaces developers need to integrate it. This is community documentation, not an official Goldsky SDK or a hosted data service.

The [repository](https://github.com/geenes/goldsky-polymarket-guide) includes local configuration generators, a read-only Python client, tests, and a [parameter-level management API reference](https://github.com/geenes/goldsky-polymarket-guide/blob/main/API_REFERENCE.md). Pair it with the [CLOB and related APIs guide](https://github.com/geenes/polymarket-clob-api-guide) for live books/trading and the [Data API guide](https://github.com/geenes/polymarket-data-api-guide) for wallet analytics.

## Contents

- [Which Goldsky interface should you use?](#which-goldsky-interface-should-you-use)
- [Polymarket V2 migration and V3 coverage](#polymarket-v2-migration-and-v3-coverage)
- [Official documentation, CLI, and SDK choices](#official-documentation-cli-and-sdk-choices)
- [Dataset selection and accounting meaning](#dataset-selection-and-accounting-meaning)
- [First Turbo pipeline](#first-turbo-pipeline)
- [Bounded backfills and live handover](#bounded-backfills-and-live-handover)
- [PostgreSQL, webhooks, and delivery correctness](#postgresql-webhooks-and-delivery-correctness)
- [Goldsky management REST API](#goldsky-management-rest-api)
- [GraphQL subgraphs and legacy migration](#graphql-subgraphs-and-legacy-migration)
- [Edge RPC, Mirror, and Compose](#edge-rpc-mirror-and-compose)
- [Data quality, joins, and reconciliation](#data-quality-joins-and-reconciliation)
- [Costs, access, and operations](#costs-access-and-operations)
- [Complete management operation inventory](#complete-management-operation-inventory)
- [Developer FAQ](#developer-faq)
- [Validation and maintenance](#validation-and-maintenance)

## Which Goldsky interface should you use?

| Need | Product/interface | What you receive or control |
| --- | --- | --- |
| Current Polymarket indexed onchain activity | Turbo curated datasets | Rows streamed to your chosen sink. |
| Filtered historical Polymarket export | Turbo fast scan and bounded job | A finite scan of a verified block interval. |
| GraphQL over a maintained subgraph | Subgraphs | Query access to entities defined by that deployment's schema. |
| Replicate subgraph entities into a database | Mirror | Subgraph-source and transform/sink workflows supported by Mirror. |
| Read blockchain state or transaction receipts | Edge RPC | JSON-RPC responses from a selected chain. |
| Manage pipelines, subgraphs, or Edge resources | Goldsky management REST | Project-scoped resource operations. |
| Durable offchain/onchain task orchestration | Compose | Application tasks, state, integrations, and execution workflows. |
| Deploy and inspect configuration from a terminal | Goldsky CLI and extensions | Project management and product-specific commands. |

These interfaces are not interchangeable endpoints for the same JSON object. A management `GET /pipelines` lists project resources; it does not download Polymarket fills. A GraphQL query reads its subgraph's entities; it does not automatically include newly deployed exchange contracts. A pipeline delivers rows to a sink you configure, where your application can query them. [Goldsky introduction](https://docs.goldsky.com/introduction), [management API overview](https://docs.goldsky.com/api-reference/overview)

Goldsky's onchain data complements the CLOB. It does not reconstruct every offchain resting order or provide an executable top-of-book quote by itself. Use CLOB REST/WebSockets for that view and index chain events for settlement and historical analysis.

## Polymarket V2 migration and V3 coverage

### Do not continue an old subgraph tutorial without checking coverage

The official migration notice is about the data source's coverage, not merely a changed query URL. A working legacy GraphQL schema, recent indexing timestamp, or non-empty result can still reflect an incomplete contract set. Record the chain, contract addresses, source start block, schema/mapping version, and latest indexed block before relying on a dataset.

For an existing application:

1. Inventory each public/private GraphQL endpoint and the queries your application uses.
2. Identify which contracts and block intervals those deployments actually index.
3. Retain historical results with their provenance; do not label them a complete current Polymarket ledger.
4. Map current requirements to the documented Turbo datasets or an explicitly maintained custom index.
5. Reconcile a small overlapping interval against chain receipts and current Polymarket APIs before switching production reads.

This is a migration procedure derived from the official deprecation notice and the difference between contract events and application-level queries.

### Four different “versions”

| Version | Example | Meaning |
| --- | --- | --- |
| Polymarket exchange generation | CTF Exchange V2 / Exchange V3 | Contract routing and order-signing compatibility. |
| Polymarket position protocol | CTF / PolyV2 | Asset and condition identity. |
| Goldsky dataset release | `polymarket.order_filled`, `2.0.0` | Selected dataset schema/implementation release. |
| Goldsky management schema | `info.version: 1.2.0`, REST base `/api/v1` | Management API specification/versioning. |

**Dataset `2.0.0` does not, by its name alone, prove Exchange V3 or every PolyV2 lifecycle event is covered.** The inspected Goldsky Polymarket page recommends its V2 datasets; it does not establish exhaustive Exchange V3 coverage. Verify supported emitter addresses, event signatures, asset mapping, and start blocks for your particular requirement. Current Polymarket SDK V3 support is documented separately in the [SDK changelog](https://docs.polymarket.com/changelog/sdks) and [contract registry](https://docs.polymarket.com/resources/contracts).

Until those checks are complete, label a report with the verified dataset/contract scope. Missing records outside that scope are “coverage unknown,” not zero activity.

## Official documentation, CLI, and SDK choices

| Tool / reference | Use | Official source |
| --- | --- | --- |
| Goldsky CLI | Authentication and project/product commands | [Installation](https://docs.goldsky.com/installation), [CLI reference](https://docs.goldsky.com/reference/cli) |
| npm `@goldskycom/cli` | Published CLI distribution | [npm](https://www.npmjs.com/package/@goldskycom/cli) |
| Turbo extension | Validate, apply, inspect, monitor pipelines | [Turbo quickstart](https://docs.goldsky.com/turbo-pipelines/quickstart), [commands](https://docs.goldsky.com/turbo-pipelines/cli-reference) |
| Compose extension | Develop and deploy Compose apps | [Compose setup](https://docs.goldsky.com/compose/quick-start) |
| REST management schema | Generate or implement a management client | [OpenAPI JSON](https://api.goldsky.com/api/v1/docs/openapi.json), [interactive API](https://api.goldsky.com/api/v1/docs) |
| GraphQL endpoint/schema | Build a client for a specific subgraph | [Endpoint documentation](https://docs.goldsky.com/subgraphs/graphql-endpoints) |
| Edge RPC | Use HTTP JSON-RPC, viem, or another compatible RPC client | [Edge quickstart](https://docs.goldsky.com/edge-rpc/quickstart) |
| Goldsky hosted documentation MCP | Connect compatible AI tools to documentation | [MCP documentation](https://docs.goldsky.com/mcp-server) |
| Platform documentation index | Locate current product guides | [llms.txt](https://docs.goldsky.com/llms.txt) |

The npm registry reported **CLI 13.10.2** on the review date. Its npm metadata did not declare an `engines` minimum; this guide therefore does not invent a Node minimum for that distribution. Follow the platform-specific installer and extension prerequisites. CLI, Turbo, and Compose extension versions should be recorded independently.

Do not confuse Goldsky infrastructure tooling with `@polymarket/client` or `polymarket-client`, which are Polymarket's own SDKs. There is no need to invent a universal “Goldsky Polymarket SDK” package: HTTP/GraphQL clients and the Goldsky CLI serve different tasks.

### Install and authenticate deliberately

The official installation page provides platform-specific installation methods. After installing, verify the actual CLI version and sign into the correct project:

```bash
goldsky --version
goldsky login
```

For headless use, the documentation supports token-based login. Keep project credentials in your normal secret store and avoid committing them to YAML or sample files. Public demo RPC keys documented by Goldsky are distinct from your private project token. [CLI installation and login](https://docs.goldsky.com/installation)

Compose currently requires an explicit `goldsky compose install`; invoking an uninstalled extension does not automatically install it. Product-specific extensions can evolve separately from the main CLI. [Compose setup](https://docs.goldsky.com/compose/quick-start)

## Dataset selection and accounting meaning

The official Polymarket integration page lists four dataset families. Choose by the question you need to answer:

| Dataset | Useful interpretation | Common mistake |
| --- | --- | --- |
| `polymarket.order_filled` | Order-level fill observations | Summing both participant perspectives as if each were independent market volume. |
| `polymarket.orders_matched` | Taker-side match aggregation | Assuming one row equals one maker fill. |
| `polymarket.user_balances` | Outcome-asset balances | Treating a balance as realized profit. |
| `polymarket.user_positions` | Position and P&L-oriented state | Treating mutable position rows as append-only fill events. |

The official example pins the order-filled dataset to `2.0.0`. Confirm the available version and schema for every dataset you use rather than applying that version to all dataset names without checking. [Dataset catalogue and migration context](https://docs.goldsky.com/chains/polymarket)

Order-filled records can represent both sides of a match, while orders-matched records describe the taker's matching activity. Before summing notional, choose a consistent economic unit—participant turnover, taker execution, or another explicitly defined measure. Do not deduplicate all records by transaction hash: multiple legitimate fills can share a transaction.

### Fields to preserve

For fill observations, retain the source row ID, block number/time, transaction hash, emitter address, asset, wallet/user, side, order identity, counterparty, maker/taker classification, quantities, fees, and builder attribution where supplied. For position state, retain the entity key and update/delete semantics as well as quantities and P&L fields.

Field names such as `amount_usdc` are historical API labels, not proof of the settlement token contract. Current Polymarket collateral documentation uses pUSD. Track collateral metadata separately. Numeric fields documented as `double` may already reflect upstream floating-point representation; parsing them into `Decimal` downstream cannot recreate precision that was previously lost.

Treat the documented schema as the starting point. Inspect actual runtime rows in a bounded project sample before writing fixed schema assumptions, null handling, or unit conversions. Preserve the source contract and dataset version with the data.

## First Turbo pipeline

The repository's [polymarket-live.yaml](https://github.com/geenes/goldsky-polymarket-guide/blob/main/polymarket-live.yaml) starts from new data and writes to a blackhole sink for inspection:

```yaml
name: polymarket-live-review
resource_size: s
sources:
  fills:
    type: dataset
    dataset_name: polymarket.order_filled
    version: 2.0.0
    start_at: latest
transforms: {}
sinks:
  review:
    type: blackhole
    from: fills
```

`start_at: latest` intentionally omits history. A blackhole sink discards output; it does not retain an analytics database. Running the pipeline can still use paid compute and source processing. This guide creates configuration files only and has not deployed them to a Goldsky account. [Turbo quickstart](https://docs.goldsky.com/turbo-pipelines/quickstart)

After installing the appropriate extension and choosing your project, validate configuration with:

```bash
goldsky turbo validate polymarket-live.yaml
```

If you choose to deploy in your own project, the documented command is `goldsky turbo apply polymarket-live.yaml`. Inspect rows and logs using the current CLI reference before replacing the blackhole sink with a persistent destination. Local YAML parsing alone is not equivalent to Goldsky CLI/service validation. [Turbo commands](https://docs.goldsky.com/turbo-pipelines/cli-reference)

## Bounded backfills and live handover

### Filter by block number for Polymarket fast scan

The Goldsky integration documentation supports fast scan for the V2 Polymarket datasets using block-number filtering. It does not support timestamp filtering for that fast-scan mode. Resolve your desired time interval into a verified Polygon block interval first and retain the mapping in your validation record.

For EVM fast-scan jobs, put both bounds in the source's `filter` expression, use `start_at: earliest`, and set top-level `job: true`. Do not copy Solana-style `end_block` into an EVM dataset configuration: the job-mode documentation says that field is not supported there. [Fast-scan sources](https://docs.goldsky.com/turbo-pipelines/sources/evm), [job-mode semantics](https://docs.goldsky.com/turbo-pipelines/job-mode)

Generate a configuration locally with your verified bounds:

```bash
export START_BLOCK='REPLACE_WITH_VERIFIED_START_BLOCK'
export END_BLOCK='REPLACE_WITH_VERIFIED_END_BLOCK'
python3 make_pipeline.py --start-block "$START_BLOCK" --end-block "$END_BLOCK" > backfill.yaml
```

The [generator](https://github.com/geenes/goldsky-polymarket-guide/blob/main/make_pipeline.py) requires integer bounds, rejects reversed/negative ranges, preserves both endpoints, and emits JSON syntax valid as YAML. It does not call Goldsky or deploy a job. Validate its output with the current CLI before deployment.

Job mode needs every source to signal completion. The current documentation describes no automatic job restart after failure and cleanup after completion; keep external evidence of job status and sink reconciliation. A process exiting is not your only completeness check.

### A defensible handover procedure

1. Define the exact dataset, version, contract scope, filters, and block interval.
2. Choose a bounded backfill interval and a live ingestion start point with a deliberate overlap.
3. Write into a destination with stable keys and correction-aware upserts; track source provenance.
4. Verify both coverage and sink checkpoint progress across the overlap.
5. Reconcile representative receipts and aggregated quantities using one consistent counting convention.
6. Switch consumers only after the required interval is confirmed; keep a record of excluded or unknown coverage.

This is an application design recommendation. It does not imply that independently deployed jobs and streams share an automatically gap-free checkpoint. Reorgs, dataset corrections, and different source configurations must be considered in the overlap policy.

## PostgreSQL, webhooks, and delivery correctness

### PostgreSQL persistence

A reviewed destination block can replace the blackhole sink:

```yaml
sinks:
  fills_db:
    type: postgres
    from: fills
    schema: analytics
    table: polymarket_fills
    secret_name: MY_POSTGRES_SECRET
    primary_key: id
    on_conflict: update
```

Create the referenced secret in your own project and ensure the writer role has the documented schema/table permissions. Do not paste connection passwords into the repository. With `primary_key` configured, the documented sink uses upsert behavior; without it, writes are plain inserts. Choose the real key for the dataset and ingestion scope. [PostgreSQL sink reference](https://docs.goldsky.com/turbo-pipelines/sinks/postgres)

An `id` key is appropriate only within the scope where the source guarantees uniqueness. If you combine networks, dataset versions, or independent deployments, preserve those dimensions rather than silently colliding rows. `on_conflict: nothing` can discard legitimate corrections; it is not interchangeable with updating mutable state.

For exact analytics, distinguish event storage from derived aggregates. A downstream SQL view can aggregate validated rows, but a blindly incremental counter can double-count replayed events or fail to reverse a deleted event. Test update/delete behavior for your chosen source and sink combination.

### Webhook delivery

A webhook sink can use a stored HTTP-auth secret:

```yaml
sinks:
  fills_webhook:
    type: webhook
    from: fills
    url: https://YOUR_RECEIVER.example/polymarket/fills
    secret_name: MY_WEBHOOK_SECRET
    one_row_per_request: false
    batch_size: 100
    batch_flush_interval: 1s
```

Goldsky documents at-least-once delivery, retries, and `2xx` acknowledgement. Batched delivery uses arrays by default; single-row mode uses an object. Acknowledge only after durable processing, tolerate retries, and do not assume exactly-once HTTP delivery. Use the documented authentication secret and avoid specifying the same auth header twice. [Webhook sink](https://docs.goldsky.com/turbo-pipelines/sinks/webhook)

Receiver design should separate authentication, payload validation, durable storage, and acknowledgement. Preserve original event IDs and operation metadata. If your configured delivery mode emits corrections/deletions, carry those into the destination model. Do not use a fill-only sample consumer for mutable balance/position data without adapting its update semantics.

### SQL and delivery limits differ by product

Turbo SQL uses its documented streaming transform subset; joins, aggregations, and window functions are not generally available in its streaming SQL mode. Perform supported filtering/projection upstream and put broader analytics in a database, a supported alternative transform, or a product designed for that work. [Turbo SQL reference](https://docs.goldsky.com/turbo-pipelines/transforms/sql)

Delivery claims should be scoped to the exact sink. “Checkpointing,” “idempotent upsert,” and “exactly-once business effect” describe different guarantees. Review retries, corrections, source ordering, and database keys together. [Turbo sink overview](https://docs.goldsky.com/turbo-pipelines/sinks/overview)

## Goldsky management REST API

**Base URL:** `https://api.goldsky.com/api/v1`. This manages resources; it is not the public GraphQL or Edge RPC URL.

Requests use `Authorization: Bearer ...` with a project-scoped token. The retrieved schema states that reads need Viewer and writes need Editor permissions. The project scope comes from the token rather than a project segment inserted into every path. [Management OpenAPI](https://api.goldsky.com/api/v1/docs/openapi.json)

```bash
curl --fail-with-body --max-time 20 --get \
  'https://api.goldsky.com/api/v1/pipelines' \
  -H "Authorization: Bearer $GOLDSKY_API_KEY" \
  --data-urlencode 'page_size=50'
```

Use your existing project credential through an appropriate secret mechanism. This guide did not create a Goldsky account or credential and did not execute authenticated management calls.

### Cursor pagination: a short page can still have more data

For the documented list operations, follow `pagination.next_page_token` as `page_token` until it is `null`. A page with fewer than `page_size` rows is not an end-of-data signal. The retrieved pipelines/subgraphs list schemas allow `page_size` 1–200 and describe a default of 50.

The read-only [Python client](https://github.com/geenes/goldsky-polymarket-guide/blob/main/goldsky_client.py) uses these rules and fails on repeated/missing cursors or an exhausted page budget:

```bash
# Requires your own project token in GOLDSKY_API_KEY.
python3 goldsky_client.py --list-pipelines
```

The client's tests exercise short pages with next tokens and explicit incomplete-result failures. They do not establish authenticated service access. A cursor belongs to its original query scope; retain filters and page policy when resuming.

### Errors and mutation boundaries

The management API documents RFC 9457 `application/problem+json`, with a stable `type` URI and human-readable details. Branch on the documented error type rather than matching English message text. Validation errors can include field-level information. A network timeout during a mutation is not proof the mutation failed; read the resulting resource state before retrying.

The operation inventory includes create, update, deploy, pause/resume, delete, log, state, webhook, and Edge-resource operations. Publishing a guide is not deploying a pipeline. The example client only reads pipeline metadata; it does not execute those management writes.

## GraphQL subgraphs and legacy migration

Goldsky subgraphs remain a platform feature. The warning above applies specifically to relying on old public Polymarket subgraphs for complete current Polymarket data; it does not mean Goldsky removed all GraphQL services.

Public endpoint pattern:

```text
https://api.goldsky.com/api/public/<project_id>/subgraphs/<name>/<version-or-tag>/gn
```

Private endpoints use `/api/private/` and the appropriate project Bearer token. A subgraph version identifies a particular deployment; a tag is an alias that can be moved. Choose immutable versions for reproducible historical work or record the resolved deployment when using tags. [GraphQL endpoints](https://docs.goldsky.com/subgraphs/graphql-endpoints), [subgraph tags](https://docs.goldsky.com/subgraphs/tags)

### Inspect the actual schema before writing queries

GraphQL entity names, field types, filter arguments, pagination, and indexing metadata depend on the deployment. A query copied from an old Polymarket subgraph is not a universal Goldsky query. Use the deployment's schema/GraphiQL interface and verify its contract coverage.

A schema-independent connectivity request is:

```json
{"query":"query ConnectivityCheck { __typename }"}
```

This only tests that a GraphQL root responds. It does not establish data freshness or correct mappings. Check GraphQL `errors` even on HTTP 200; partial `data` must not silently become a complete export. The included `decode_graphql` helper rejects such partial-success payloads.

Use the schema's supported ordering and filtering for pagination; do not assume all GraphQL endpoints share REST's `page_token`, a default page size, or support for `id_gt`. For reproducibility, use block-pinned querying only when the specific schema supports it and record the block hash/number and indexing status.

The current endpoint documentation lists a default public rate limit of 50 requests per ten seconds, subject to project/service policy. That figure is for the documented public GraphQL interface—not a universal management, Turbo, or Edge limit. The official community Uniswap endpoint used as an example in that page returned 403 during this review; it was not used as proof of a working current Polymarket data source.

## Edge RPC, Mirror, and Compose

### Edge RPC: chain-level reads

Edge uses JSON-RPC on a selected chain. A transaction receipt can help reconcile indexed contract events; it will not supply Gamma market titles or the full offchain book. The official quickstart exposes a public demo key for testing:

```bash
curl --fail-with-body --max-time 20 \
  'https://edge.goldsky.com/standard/evm/1?key=demo' \
  -H 'Content-Type: application/json' \
  --data '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

This example reads **Ethereum chain 1**, not Polygon. It was executed successfully to verify Edge connectivity. For Polymarket reconciliation, select a currently supported Polygon endpoint and the intended network explicitly. Decode hexadecimal quantities and check the JSON-RPC `error` field independently of the HTTP status. [Edge quickstart](https://docs.goldsky.com/edge-rpc/quickstart)

The included `python3 goldsky_client.py` executes only this demo block-height read by default. Account keys belong in your normal secret handling. Edge's documented per-key/per-IP limits differ from GraphQL quotas; avoid exposing credential-bearing URLs in logs. [Edge access and limits](https://docs.goldsky.com/edge-rpc/platform/security)

### Mirror versus Turbo

Mirror and Turbo are separate pipeline formats and execution systems. Mirror uses `apiVersion: 3`; Turbo does not use that field. Mirror commands use `goldsky pipeline ...`, while Turbo uses `goldsky turbo ...`. Mirror supports subgraph-entity sources that the comparison page does not list as Turbo sources. Do not translate YAML by renaming the CLI command alone. [Mirror/Turbo comparison](https://docs.goldsky.com/mirror-vs-turbo)

Choose based on the required source, transform semantics, sink, and recovery model. For current Polymarket curated data, begin with the documented Turbo recommendation. For your own maintained subgraph entities, Mirror may be the relevant replication path.

### Compose: durable application workflows

Compose orchestrates application tasks that interact with data, HTTP services, state, and onchain operations. It is not a replacement for a dataset schema or query endpoint. Goldsky publishes a Polymarket copy-trader tutorial, but automatic execution introduces a separate signing, wallet, order, and reconciliation workflow. This guide does not deploy or run that tutorial. [Compose overview](https://docs.goldsky.com/compose/introduction), [official Polymarket example](https://docs.goldsky.com/compose/guides/build-a-polymarket-copy-trader)

For analytics, a first useful Compose integration could process a validated webhook into a durable application task. Keep event observation separate from any authorization to place orders. Task retry semantics do not automatically make every external side effect idempotent.

## Data quality, joins, and reconciliation

A useful Polymarket indexing record should let another developer answer these questions:

| Dimension | Evidence to retain |
| --- | --- |
| Coverage | Network, emitter contracts, event signatures, dataset/version, block bounds. |
| Identity | Source ID, transaction hash, asset/condition mapping, wallet, maker/taker perspective. |
| Freshness | Source observation time, chain/indexing lag, destination checkpoint. |
| Finality/corrections | Relevant block hash, reorg/update/delete behavior, correction status. |
| Units | Collateral contract, base-unit versus display-unit quantities, numeric representation. |
| Completeness | Filters, upper/lower bounds, terminal cursor/checkpoint or explicit incomplete status. |
| Provenance | Source schema/configuration fingerprint and ingestion run identifier. |

Join Gamma metadata through explicit condition/asset mappings. Preserve CTF token IDs and PolyV2 position IDs as strings. Do not convert an asset to JavaScript `Number`, truncate a condition hash, or join markets solely by title. A signer wallet and position-holding wallet can differ; preserve both roles when available.

For reconciliation, choose a small verified block window and compare representative decoded events to receipts, then compare aggregates using the same participant/taker convention, collateral units, fees, and lifecycle scope. Compare against Data API as a separate indexed view, not as an unquestionable instantaneous chain ledger. Report lag and scope differences before treating mismatches as incorrect balances.

A rolling balance table is not enough to recompute every historical P&L methodology. Store the required event history and define treatment of transfers, redemptions, splits/merges, rewards, fees, and corrections. Where the source does not cover those events or their semantics are unknown, limit the claim rather than manufacturing a precise profit number.

These storage and validation procedures are engineering recommendations derived from the interface differences, not official Goldsky accounting guarantees.

## Costs, access, and operations

Backfills can process far more rows than a live dashboard normally consumes. Begin with a small bounded interval, inspect source/sink throughput, and estimate retained storage and query workload before a broad historical scan. The official Polymarket page specifically notes large balance/position datasets; “only one pipeline” is not a useful cost estimate.

Cost drivers vary across Subgraphs, Turbo, Mirror, Edge, Compose, and hosted databases. Review the current [pricing documentation](https://docs.goldsky.com/pricing/summary) and your project plan. The documented Goldsky-hosted Postgres path requires Scale or above; a blackhole sink does not make compute free. This publication did not create billable resources.

Track source lag, throughput, errors, checkpoints, sink acknowledgements, failed jobs, restarts, and configuration versions. `pause`, `resume`, and `restart` are different operations. In particular, clearing state can reprocess history; do not use a state-clearing restart as a routine response to every warning. Job-mode restart and cleanup semantics differ from continuous deployments. [Turbo operations](https://docs.goldsky.com/turbo-pipelines/cli-reference)

Use distinct names for development and production resources, protect secrets, and review access by project. When sharing debug evidence, include sanitized errors, source version, time/block scope, and config shape without tokens, connection strings, or customer rows.

## Complete management operation inventory

The retrieved management OpenAPI schema is version `1.2.0` and contains **40 operations across 31 paths**. The [parameter-level reference](https://github.com/geenes/goldsky-polymarket-guide/blob/main/API_REFERENCE.md) includes required inputs and constraints. This is the management API inventory, not a list of all Goldsky datasets or GraphQL entity queries.

### Goldsky management

[Official specification](https://api.goldsky.com/api/v1/docs/openapi.json) · 31 paths · 40 operations.

| Method | Path | Operation ID |
| --- | --- | --- |
| `GET` | `/pipelines` | `listPipelines` |
| `POST` | `/pipelines` | `createPipeline` |
| `GET` | `/pipelines/{name}` | `getPipeline` |
| `DELETE` | `/pipelines/{name}` | `deletePipeline` |
| `POST` | `/pipelines/validate` | `validatePipeline` |
| `POST` | `/pipelines/preview` | `previewPipeline` |
| `PUT` | `/pipelines/{name}/pause` | `pausePipeline` |
| `PUT` | `/pipelines/{name}/resume` | `resumePipeline` |
| `PUT` | `/pipelines/{name}/restart` | `restartPipeline` |
| `GET` | `/pipelines/{name}/logs` | `getPipelineLogs` |
| `GET` | `/pipelines/{name}/logs/error-count` | `getPipelineErrorCount` |
| `GET` | `/pipelines/{name}/status` | `getPipelineStatus` |
| `GET` | `/pipelines/{name}/state` | `getPipelineState` |
| `GET` | `/subgraphs` | `listSubgraphs` |
| `GET` | `/subgraphs/{name}` | `getSubgraph` |
| `GET` | `/subgraphs/supported-chains` | `listSubgraphChains` |
| `GET` | `/subgraphs/{name}/{version}` | `getSubgraphVersion` |
| `PATCH` | `/subgraphs/{name}/{version}` | `updateSubgraphVersion` |
| `GET` | `/subgraphs/{name}/{version}/logs` | `getSubgraphLogs` |
| `PUT` | `/subgraphs/{name}/{version}/pause` | `pauseSubgraph` |
| `PUT` | `/subgraphs/{name}/{version}/resume` | `resumeSubgraph` |
| `PUT` | `/subgraphs/{name}/tags/{version}` | `setSubgraphTag` |
| `DELETE` | `/subgraphs/{name}/tags/{version}` | `deleteSubgraphTag` |
| `DELETE` | `/subgraphs/{name}/deployments/{version}` | `deleteSubgraphDeployment` |
| `PUT` | `/subgraphs/{name}/deployments/{version}` | `deploySubgraph` |
| `GET` | `/subgraphs/webhooks` | `listWebhooks` |
| `POST` | `/subgraphs/webhooks` | `createWebhook` |
| `DELETE` | `/subgraphs/webhooks/{name}` | `deleteWebhook` |
| `GET` | `/subgraphs/{name}/{version}/entities` | `listWebhookEntities` |
| `GET` | `/edge/networks` | `listEdgeNetworks` |
| `GET` | `/edge/sources` | `listEdgeSources` |
| `GET` | `/edge` | `listEdgeEndpoints` |
| `POST` | `/edge` | `createEdgeEndpoint` |
| `GET` | `/edge/{name}` | `getEdgeEndpoint` |
| `PATCH` | `/edge/{name}` | `updateEdgeEndpoint` |
| `DELETE` | `/edge/{name}` | `deleteEdgeEndpoint` |
| `PUT` | `/edge/{name}/pause` | `pauseEdgeEndpoint` |
| `PUT` | `/edge/{name}/resume` | `resumeEdgeEndpoint` |
| `GET` | `/edge/{name}/api-key` | `revealEdgeEndpointKey` |
| `GET` | `/edge/{name}/metrics` | `getEdgeEndpointMetrics` |

## Developer FAQ

### What is the current Goldsky endpoint for Polymarket trades?

The official integration recommends Turbo V2 datasets streamed into your own sink. That is a pipeline workflow, not a universal replacement public REST/GraphQL URL for every trade query. Use your chosen sink/query layer or Polymarket's own APIs according to the requirement.

### Are old Polymarket Goldsky subgraphs still reliable?

Goldsky's current notice says they can return incomplete or incorrect data after the April 2026 migration. Verify historical scope and current contract coverage before relying on them.

### Does dataset version 2.0.0 prove Exchange V3 coverage?

No. Dataset releases and exchange generations are distinct. Check the included contracts, events, and block ranges explicitly.

### Can I use Turbo for a one-time Polymarket backfill?

The documented fast-scan/job approach uses a bounded block-number filter and a completion-capable source. For EVM datasets, do not assume Solana-style `end_block` applies. Validate the generated config before deployment.

### Why is my trade volume doubled?

One possible cause is summing both order-filled participant perspectives. Define the intended counting unit and compare with taker-side match semantics. Multiple rows in one transaction are not necessarily duplicates.

### Can I stop pagination when a management page is short?

No. Continue until `pagination.next_page_token` is null. The supplied client tests this case.

### Do I need a Goldsky SDK?

Use the CLI for resource workflows, the OpenAPI schema for REST clients, the target subgraph schema for GraphQL clients, and standard RPC libraries for Edge. Polymarket SDKs serve the exchange/API integration, not Goldsky resource management.

### Were these pipelines deployed and validated against a live Goldsky account?

No. The files were created and locally checked. Public Edge RPC was tested; authenticated management calls, Turbo deployment, live Polymarket dataset rows, and sink behavior require validation in your own project.

## Validation and maintenance

See [VALIDATION.md](https://github.com/geenes/goldsky-polymarket-guide/blob/main/VALIDATION.md) for retrieved-source fingerprints, successful/failed public checks, local test results, and untested behavior. The guide keeps official documentation claims separate from live observations.

For updates, check the [Goldsky documentation index](https://docs.goldsky.com/llms.txt), [Polymarket indexing notice](https://docs.goldsky.com/chains/polymarket), management schema, CLI/extension versions, and the source contract set. Record the date and scope of each review. Submit corrections through [repository issues](https://github.com/geenes/goldsky-polymarket-guide/issues) with reproducible sanitized evidence.

The explanations and local examples are independently written. Clear answers, explicit version labels, reference tables, and primary sources make the guide easier to find and cite; publication alone does not establish search ranking or AI citation outcomes.
