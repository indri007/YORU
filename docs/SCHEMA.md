# Data Schema

## 1. Audit Event (JSON Log Format)
| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `auid` | String | Yes | Original authenticated user ID (e.g., `1000`) |
| `uid` | String | Yes | Effective user ID (e.g., `0` for root) |
| `comm` | String | Yes | Command executed (e.g., `nano`) |
| `path` | String | Yes | File modified (e.g., `/etc/passwd`) |
| `key` | String | Yes | Audit rule key (e.g., `yoru_kontrol`) |

## 2. Environment Configuration (`.env`)
- `GEMINI_API_KEY`: Secret string.
- `LISTEN_HOST`: IP Address string (default `127.0.0.1`).
- `LISTEN_PORT`: Integer (default `8080`).

## 3. yoru-model-proxy Payload
**Request:**
```json
{
  "messages": [{"role": "user", "content": "Analyze this event..."}],
  "max_tokens": 512
}
```
**Response:**
```json
{
  "choices": [{"message": {"content": "User jevin edited sudoers."}}]
}
```
