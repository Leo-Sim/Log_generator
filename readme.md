# Log Generator
### Lightweight  sample log generator for testing SIEM system.
This module generates sample logs and supports sending them to external servers via TCP connections.

Currently supported log formats:
- LEEF (Log Event Extended Format)
- CEF (Common Event Format)
- Custom-defined formats 


### This module works based on configuration files located in 
- `config/config.yaml` — Configuration file for log type, target servers, and transmission frequency  
- `config/log_format/cef.json` — Detailed field configuration for CEF logs  
- `config/log_format/leef.json` — Detailed field configuration for LEEF logs  
- `config/log_format/custom.json` — Detailed field configuration for custom-formatted logs  

--
## config/config.yaml
###  Top-level Fields

| Field | Description | Example |
|-------|-------------|---------|
| `log-type` | The format of logs to generate. Supported values: `custom`, `leef`, `cef`. | `"leef"` |

---

###  `transfer` Section

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
| `fields`           | List of field objects to include in each log entry.               | `[{"name": "sip", "value": [...]}, ...]`      |
| `fields[].name`    | Name of the field (e.g., `"time_stamp"`, `"sip"`, `"sport"`).     | `"sip"`                                       |
| `fields[].value`   | List of possible values randomly chosen for that field.           | `["1.2.1.2", "121.31.67.20", "100.20.100.45"]` |

---

### leef.json
| Field         | Description                                                              | Example                                          |
|---------------|--------------------------------------------------------------------------|--------------------------------------------------|
| `version`     | LEEF format version.                                                     | `"2.0"`                                          |
| `delimiter`   | Delimiter used between key-value pairs in the log body.                  | `"^"`                                            |
| `header`      | A list of metadata fields to be included in the LEEF header.             | `[{"name": "vendor", "value": [...]}, ...]`      |
| `header[].name`  | Name of the header field (e.g., vendor, product).                     | `"vendor"`                                       |
| `header[].value` | Possible values randomly chosen for this header field.                | `["logCompany", "Ztech"]`                        |
| `fields`      | A list of key-value fields to include in the log body.                   | `[{"name": "sip", "value": [...]}, ...]`         |
| `fields[].name`  | Name of the field in the log body (e.g., sip, dip, time_stamp).       | `"time_stamp"`                                   |
| `fields[].value` | Possible values randomly chosen for this log field.                   | `["2019-02-05 16:20:22", "2019-11-02 10:29:21"]` |

---

### cef.json

| Field              | Description                                                              | Example                                       |
|--------------------|--------------------------------------------------------------------------|-----------------------------------------------|
| `version`          | Log format version of this JSON schema (not related to CEF header).     | `"2.0"`                                       |
| `delimiter`        | Delimiter used between key-value pairs in the log body.                 | `"^"`                                         |
| `header`           | A list of metadata fields used to construct the CEF header.             | `[{"name": "vendor", "value": [...]}, ...]`   |
| `header[].name`    | Name of the CEF header field (e.g., `"vendor"`, `"signature"`).         | `"vendor"`                                    |
| `header[].value`   | List of possible values randomly selected for that field.               | `["AhnLab", "Secuve"]`                         |
| `fields`           | List of key-value fields to include in the log body.                    | `[{"name": "sip", "value": [...]}, ...]`      |
| `fields[].name`    | Name of the field (e.g., `"rt"`, `"sip"`, `"sport"`).                   | `"rt"`                                        |
| `fields[].value`   | List of possible values randomly chosen for the field.                  | `["2019-02-05 16:20:22", "2019-11-02 10:29:21"]` |

---


📝 **Tip**: You can switch between `leef.json`, `custom.json`, or other formats by changing `log_format_type` and `log_format_path` in `config.yaml`.

