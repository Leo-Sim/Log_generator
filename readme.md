# Log Generator

This module generates sample logs and supports sending them to external servers.

Currently supported log formats:
- LEEF (Log Event Extended Format)
- Custom-defined formats


- - CEF (Common Event Format) will be added to this project


--
### 🔧 Top-level Fields

| Field | Description | Example |
|-------|-------------|---------|
| `log-type` | The format of logs to generate. Supported values: `custom`, `leef`, `cef`. | `"leef"` |

---

### 🔁 `transfer` Section

| Field | Description | Example |
|-------|-------------|---------|
| `interval` | Time interval (in seconds) between each batch transmission. | `5` |
| `count` | Number of logs to generate per interval. | `2` |
| `target-servers` |  list of IP:PORT pairs to which logs will be sent. | `"127.0.0.1:15002,11.12.13.22:14028"` |

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

### 🔧 Top-level Fields

| Field | Description | Example |
|-------|-------------|---------|
| `version` | LEEF format version. | `"2.0"` |
| `delimiter` | Delimiter used between key-value pairs in the log body. | `"^"` |

---

### 🧩 `header` (LEEF Header Fields)

This is a list of field definitions used to build the LEEF log prefix:

| Name | Description | Example Values |
|------|-------------|----------------|
| `vendor` | Vendor or manufacturer name. | `"ASecurity"`, `"AhnLab"` |
| `product` | Product name that generated the log. | `"SIEM"`, `"ThreatDetector"` |
| `product_version` | Version of the logging product. | `"1.0.0"`, `"2.1.2"` |
| `event_id` | Event ID or type identifier. | `"2020"`, `"3012"` |



---

### 🗂 `fields` (Log Body Fields)

This section defines the key-value data that follows the LEEF header.

| Name | Description | Example Values |
|------|-------------|----------------|
| `name` | Name of the field (e.g., `"timestamp"`, `"sip"`, `"sport"`) |
| `value` | List of possible values to randomly choose from |

Each field’s `value` array is used to randomly generate realistic variations of logs.

---


📝 **Tip**: You can switch between `leef.json`, `custom.json`, or other formats by changing `log_format_type` and `log_format_path` in `config.yaml`.

