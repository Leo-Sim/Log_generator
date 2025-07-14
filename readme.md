# Log Generator

This module generates sample logs and supports sending them to external servers.

Currently supported log formats:
- LEEF (Log Event Extended Format)
- CEF (Common Event Format)
- Custom-defined formats



---

### 🔧 `config.yaml`

Defines global settings for log generation and transmission.

| Field | Description | Example |
|-------|-------------|---------|
| `log_format_type` | Type of log format to use (e.g., leef, custom, cef) | `"leef"` |
| `log_format_path` | Path to the log format definition JSON file | `"./config/leef.json"` |
| `generate_mode` | Log generation mode: `"batch"` or `"realtime"` | `"batch"` |
| `generate_num` | Number of logs per batch (if in batch mode) | `10` |
| `generate_interval` | Interval in seconds between transmissions | `5` |
| `target_servers` | Comma-separated list of IP and port targets | `"127.0.0.1:5140,192.168.1.100:1514"` |

---

### 📄 `custom.json`

Defines the structure and content for a custom log format.

| Field | Description |
|-------|-------------|
| `include_field_header` | Whether to include the field header line (`True`/`False`) |
| `header_separator` | Separator between the header and log body | `"--"` |
| `delimiter` | Delimiter used between field values | ```"`"``` |
| `header` | Prefix used at the beginning of each log | `"#"` |
| `footer` | Suffix used at the end of each log | `"!"` |
| `fields` | List of field objects to include in each log |
| → `name` | Name of the field (e.g., `"timestamp"`, `"sip"`, `"sport"`) |
| → `value` | List of possible values to randomly choose from |

---

### 📄 `leef.json`

Defines the structure for LEEF-formatted logs (Log Event Extended Format).

| Field | Description |
|-------|-------------|
| `version` | LEEF version (e.g., `"2.0"`) |
| `vendor` | Product vendor name | `"MyCompany"` |
| `product` | Product name | `"LogGenerator"` |
| `product_version` | Version of the product | `"1.0"` |
| `event_id` | Event type ID or name | `"login_attempt"` |
| `delimiter` | Delimiter between key-value fields | `"\t"` |
| `fields` | Key-value field definitions for the log |
| → `name` | Field name (e.g., `"src"`, `"dst"`, `"protocol"`) |
| → `value` | List of possible values for that field |

---

📝 **Tip**: You can switch between `leef.json`, `custom.json`, or other formats by changing `log_format_type` and `log_format_path` in `config.yaml`.

