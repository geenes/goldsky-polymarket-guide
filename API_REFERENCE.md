# API operation and parameter reference

Reviewed September 7, 2026. This is a mechanical inventory of the retrieved official schemas. A missing security declaration does not prove an endpoint is public. Method names do not determine whether an operation changes state. Follow the linked source and the main guide for authentication and execution semantics.

## Goldsky management

Source: [Goldsky management specification](https://api.goldsky.com/api/v1/docs/openapi.json). Schema version: `1.2.0`.

<a id="goldsky-management-get--pipelines"></a>

### GET `/pipelines`

Operation: `listPipelines`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `type` | query | no | string |
| `page_size` | query | no | integer; minimum=1, maximum=200 |
| `page_token` | query | no | string |
| `pageSize` | query | no | integer; minimum=1, maximum=200 |
| `pageToken` | query | no | string |

Documented status codes: `200`.

<a id="goldsky-management-post--pipelines"></a>

### POST `/pipelines`

Operation: `createPipeline`.

Security declaration: `[{"BearerAuth": []}]`.

Request body `application/json`: object; required=true.

| Body field | Required | Type and schema constraints |
| --- | --- | --- |
| `name` | no | string; minLength=1, maxLength=50 |
| `resource_size` | no | string |
| `description` | no | string |
| `use_dedicated_ip` | no | boolean |
| `definition` | yes | object |

Documented status codes: `200`.

<a id="goldsky-management-get--pipelines--name"></a>

### GET `/pipelines/{name}`

Operation: `getPipeline`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-delete--pipelines--name"></a>

### DELETE `/pipelines/{name}`

Operation: `deletePipeline`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-post--pipelines-validate"></a>

### POST `/pipelines/validate`

Operation: `validatePipeline`.

Security declaration: `[{"BearerAuth": []}]`.

Request body `application/json`: object; required=true.

| Body field | Required | Type and schema constraints |
| --- | --- | --- |
| `name` | no | string |
| `resource_size` | no | string |
| `description` | no | string |
| `use_dedicated_ip` | no | boolean |
| `definition` | yes | object |

Documented status codes: `200`.

<a id="goldsky-management-post--pipelines-preview"></a>

### POST `/pipelines/preview`

Operation: `previewPipeline`.

Security declaration: `[{"BearerAuth": []}]`.

Request body `application/json`: object; required=true.

| Body field | Required | Type and schema constraints |
| --- | --- | --- |
| `definition` | yes | object |
| `ttl_seconds` | no | number; minimum=1, maximum=600 |

Documented status codes: `200`.

<a id="goldsky-management-put--pipelines--name--pause"></a>

### PUT `/pipelines/{name}/pause`

Operation: `pausePipeline`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-put--pipelines--name--resume"></a>

### PUT `/pipelines/{name}/resume`

Operation: `resumePipeline`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-put--pipelines--name--restart"></a>

### PUT `/pipelines/{name}/restart`

Operation: `restartPipeline`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |

Request body `application/json`: object; required=false.

| Body field | Required | Type and schema constraints |
| --- | --- | --- |
| `clearState` | no | boolean; default=false |

Documented status codes: `200`.

<a id="goldsky-management-get--pipelines--name--logs"></a>

### GET `/pipelines/{name}/logs`

Operation: `getPipelineLogs`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `logLevels` | query | no | string |
| `cursor` | query | no | number |
| `after` | query | no | number |
| `search` | query | no | string |
| `direction` | query | no | union |
| `name` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-get--pipelines--name--logs-error-count"></a>

### GET `/pipelines/{name}/logs/error-count`

Operation: `getPipelineErrorCount`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `since_hours` | query | no | integer; default=6, minimum=1, maximum=168 |
| `name` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-get--pipelines--name--status"></a>

### GET `/pipelines/{name}/status`

Operation: `getPipelineStatus`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-get--pipelines--name--state"></a>

### GET `/pipelines/{name}/state`

Operation: `getPipelineState`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-get--subgraphs"></a>

### GET `/subgraphs`

Operation: `listSubgraphs`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `page_size` | query | no | integer; minimum=1, maximum=200 |
| `page_token` | query | no | string |

Documented status codes: `200`.

<a id="goldsky-management-get--subgraphs--name"></a>

### GET `/subgraphs/{name}`

Operation: `getSubgraph`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-get--subgraphs-supported-chains"></a>

### GET `/subgraphs/supported-chains`

Operation: `listSubgraphChains`.

Security declaration: `[{"BearerAuth": []}]`.

Documented status codes: `200`.

<a id="goldsky-management-get--subgraphs--name---version"></a>

### GET `/subgraphs/{name}/{version}`

Operation: `getSubgraphVersion`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |
| `version` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-patch--subgraphs--name---version"></a>

### PATCH `/subgraphs/{name}/{version}`

Operation: `updateSubgraphVersion`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |
| `version` | path | yes | string |

Request body `application/json`: object; required=false.

| Body field | Required | Type and schema constraints |
| --- | --- | --- |
| `public_endpoint_enabled` | no | boolean |
| `private_endpoint_enabled` | no | boolean |
| `description` | no | string; maxLength=500 |

Documented status codes: `200`.

<a id="goldsky-management-get--subgraphs--name---version--logs"></a>

### GET `/subgraphs/{name}/{version}/logs`

Operation: `getSubgraphLogs`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `cursor` | query | no | number |
| `after` | query | no | number |
| `direction` | query | no | union |
| `search` | query | no | string |
| `log_level` | query | no | string |
| `log_levels` | query | no | string |
| `name` | path | yes | string |
| `version` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-put--subgraphs--name---version--pause"></a>

### PUT `/subgraphs/{name}/{version}/pause`

Operation: `pauseSubgraph`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |
| `version` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-put--subgraphs--name---version--resume"></a>

### PUT `/subgraphs/{name}/{version}/resume`

Operation: `resumeSubgraph`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |
| `version` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-put--subgraphs--name--tags--version"></a>

### PUT `/subgraphs/{name}/tags/{version}`

Operation: `setSubgraphTag`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |
| `version` | path | yes | string |

Request body `application/json`: object; required=true.

| Body field | Required | Type and schema constraints |
| --- | --- | --- |
| `target_version` | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-delete--subgraphs--name--tags--version"></a>

### DELETE `/subgraphs/{name}/tags/{version}`

Operation: `deleteSubgraphTag`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |
| `version` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-delete--subgraphs--name--deployments--version"></a>

### DELETE `/subgraphs/{name}/deployments/{version}`

Operation: `deleteSubgraphDeployment`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |
| `version` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-put--subgraphs--name--deployments--version"></a>

### PUT `/subgraphs/{name}/deployments/{version}`

Operation: `deploySubgraph`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |
| `version` | path | yes | string |

Request body `multipart/form-data`: object; required=false.

| Body field | Required | Type and schema constraints |
| --- | --- | --- |
| `bundle` | no | object |
| `overwrite` | no | object |
| `remove_graft` | no | object |
| `skip_graft_validation` | no | object |
| `start_block` | no | object |
| `graft_from` | no | object |
| `description` | no | object |
| `graph_node_shard` | no | object |

Documented status codes: `201`.

<a id="goldsky-management-get--subgraphs-webhooks"></a>

### GET `/subgraphs/webhooks`

Operation: `listWebhooks`.

Security declaration: `[{"BearerAuth": []}]`.

Documented status codes: `200`.

<a id="goldsky-management-post--subgraphs-webhooks"></a>

### POST `/subgraphs/webhooks`

Operation: `createWebhook`.

Security declaration: `[{"BearerAuth": []}]`.

Request body `application/json`: object; required=true.

| Body field | Required | Type and schema constraints |
| --- | --- | --- |
| `name` | yes | string; maxLength=42 |
| `subgraph_name` | yes | string |
| `subgraph_version` | yes | string |
| `entity` | yes | string |
| `webhook_url` | yes | string |
| `secret` | no | string |
| `num_retries` | no | integer; minimum=0, maximum=10 |
| `retry_interval_seconds` | no | integer; minimum=1 |
| `retry_timeout_seconds` | no | integer; minimum=1 |

Documented status codes: `200`.

<a id="goldsky-management-delete--subgraphs-webhooks--name"></a>

### DELETE `/subgraphs/webhooks/{name}`

Operation: `deleteWebhook`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-get--subgraphs--name---version--entities"></a>

### GET `/subgraphs/{name}/{version}/entities`

Operation: `listWebhookEntities`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string |
| `version` | path | yes | string |

Documented status codes: `200`.

<a id="goldsky-management-get--edge-networks"></a>

### GET `/edge/networks`

Operation: `listEdgeNetworks`.

Security declaration: `[{"BearerAuth": []}]`.

Documented status codes: `200`.

<a id="goldsky-management-get--edge-sources"></a>

### GET `/edge/sources`

Operation: `listEdgeSources`.

Security declaration: `[{"BearerAuth": []}]`.

Documented status codes: `200`.

<a id="goldsky-management-get--edge"></a>

### GET `/edge`

Operation: `listEdgeEndpoints`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `product` | query | no | union |

Documented status codes: `200`.

<a id="goldsky-management-post--edge"></a>

### POST `/edge`

Operation: `createEdgeEndpoint`.

Security declaration: `[{"BearerAuth": []}]`.

Request body `application/json`: object; required=true.

| Body field | Required | Type and schema constraints |
| --- | --- | --- |
| `name` | yes | string; minLength=1 |
| `product` | no | union |
| `rate_limit_budget` | no | string; enum=["edge-tier-6krpm-total-unlimited-per-ip", "edge-tier-60krpm-total-unlimited-per-ip", "edge-tier-180krpm-total-unlimited-per-ip", "edge-tier-360krpm-total-unlimited-per-ip", "edge-tier-600krpm-total-unlimited-per-ip", "edge-tier-6krpm-total-500rpm-per-ip", "edge-tier-60krpm-total-500rpm-per-ip", "edge-tier-180krpm-total-500rpm-per-ip", "edge-tier-360krpm-total-500rpm-per-ip", "edge-tier-600krpm-total-500rpm-per-ip", "edge-tier-unlimited-total-100rpm-per-ip", "edge-tier-unlimited-total-500rpm-per-ip"] |
| `allowed_domains` | no | array[string] |

Documented status codes: `201`.

<a id="goldsky-management-get--edge--name"></a>

### GET `/edge/{name}`

Operation: `getEdgeEndpoint`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string; minLength=1 |

Documented status codes: `200`.

<a id="goldsky-management-patch--edge--name"></a>

### PATCH `/edge/{name}`

Operation: `updateEdgeEndpoint`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string; minLength=1 |

Request body `application/json`: object; required=false.

| Body field | Required | Type and schema constraints |
| --- | --- | --- |
| `rate_limit_budget` | no | union |
| `allowed_domains` | no | array[string] |

Documented status codes: `200`.

<a id="goldsky-management-delete--edge--name"></a>

### DELETE `/edge/{name}`

Operation: `deleteEdgeEndpoint`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string; minLength=1 |

Documented status codes: `204`.

<a id="goldsky-management-put--edge--name--pause"></a>

### PUT `/edge/{name}/pause`

Operation: `pauseEdgeEndpoint`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string; minLength=1 |

Documented status codes: `200`.

<a id="goldsky-management-put--edge--name--resume"></a>

### PUT `/edge/{name}/resume`

Operation: `resumeEdgeEndpoint`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string; minLength=1 |

Documented status codes: `200`.

<a id="goldsky-management-get--edge--name--api-key"></a>

### GET `/edge/{name}/api-key`

Operation: `revealEdgeEndpointKey`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `name` | path | yes | string; minLength=1 |

Documented status codes: `200`.

<a id="goldsky-management-get--edge--name--metrics"></a>

### GET `/edge/{name}/metrics`

Operation: `getEdgeEndpointMetrics`.

Security declaration: `[{"BearerAuth": []}]`.

| Parameter | In | Required | Type and schema constraints |
| --- | --- | --- | --- |
| `from` | query | no | string date-time |
| `to` | query | no | string date-time |
| `bucket_size` | query | no | union |
| `name` | path | yes | string; minLength=1 |

Documented status codes: `200`.
