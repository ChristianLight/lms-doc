# SourceRegion

Exact occurrence and evidence locator within one immutable extraction revision.

Owned by **curriculum**.

## Fields

### id

Stable opaque identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### extraction_run_id

Protected parent extraction.

Required. Null is rejected.

References [SourceExtractionRun](SourceExtractionRun.md). Must resolve to an authorized SourceExtractionRun in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### page_index

Zero-based physical PDF page index.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 100000
}
```

### ordinal

Stable region order within accepted page receipt.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 200000
}
```

### bbox_mpt

Upright cropped page rectangle x0, y0, x1, y1 in integer milli-points.

Required. Null is rejected.

```json
{
  "type": "array",
  "prefixItems": [
    {
      "type": "integer",
      "minimum": 0,
      "maximum": 28800000
    },
    {
      "type": "integer",
      "minimum": 0,
      "maximum": 28800000
    },
    {
      "type": "integer",
      "minimum": 0,
      "maximum": 28800000
    },
    {
      "type": "integer",
      "minimum": 0,
      "maximum": 28800000
    }
  ],
  "minItems": 4,
  "maxItems": 4,
  "items": false
}
```

### kind

Semantic region kind.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "text",
    "heading",
    "table",
    "table_cell",
    "form_field",
    "figure",
    "caption",
    "equation",
    "footnote",
    "artifact"
  ]
}
```

### method

Accepted extraction or transcription method.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "text_layer",
    "tagged_text",
    "ocr",
    "vector_geometry",
    "transcription",
    "math_recognition"
  ]
}
```

### review_state

Region decision pinned in the extraction revision.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "candidate",
    "needs_review",
    "accepted",
    "excluded"
  ]
}
```

### confidence_permille

Optional OCR engine signal, not a correctness guarantee.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 1000
}
```

### evidence_object_id

Protected page evidence shard with raw and normalized representations.

Required. Null is rejected.

References [StorageObject](StorageObject.md). Same institution. Platform purpose evidence and exact owner SourceExtractionRun. Resolve actual object version and digest before use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### evidence_path

RFC 6901 JSON Pointer into exact evidence shard.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 500
}
```

### payload_digest

Canonical accepted region content and geometry digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### created_at

Accepted extraction write instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### sensitivity

Minimum protected retrieval and crop restriction.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "authoring_only",
    "answer_key",
    "restricted_rights",
    "personal_data"
  ],
  "default": "authoring_only"
}
```

## Integrity

- Rectangle positive area and fully inside reviewed upright page extent.
- Review never discloses protected region bytes through metadata or event payload.
- Regions are referenced only when accepted by a sealed extraction.
- If a page shard contains a restricted region, full shard retrieval requires the strongest applicable authority. A weaker scope receives only an independently approved redacted rendition, never its underlying object ID.

## Unique keys

- `id`
- `extraction_run_id, page_index, ordinal`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| extraction_run_id, page_index, ordinal | Protected source page navigation and review. |
| extraction_run_id, review_state, kind | Review consequential regions and missing evidence. |

## Retention

Retain protected decisions while needed for reviewed source derivation and retention policy or hold. Retain authorized academic lineage tombstone after eligible source disposition.
