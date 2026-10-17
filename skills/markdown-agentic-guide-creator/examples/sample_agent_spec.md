# SPECIFICATION: Example Authentication Microservice

> **Agent Ingestion Specification Package**  
> Auto-generated for autonomous coding agents (Antigravity, Gemini CLI, Claude Code).

## Executive Architecture Summary
Demonstration of an unclipped, machine-parseable Markdown specification packaging an auth service and its configuration file.

## Packaged Files Index
| Index | Target File Path | Language | Size (bytes) |
| :---: | :--- | :---: | :---: |
| 1 | `src/auth.py` | `py` | 520 |
| 2 | `config/settings.json` | `json` | 145 |

---

## Delimited Source Modules

=== BEGIN FILE: src/auth.py (py) ===
````py
import hmac
import hashlib
import time

def generate_token(user_id: str, secret: str) -> str:
    timestamp = str(int(time.time()))
    signature = hmac.new(
        secret.encode(),
        f"{user_id}:{timestamp}".encode(),
        hashlib.sha256
    ).hexdigest()
    return f"{user_id}.{timestamp}.{signature}"

def verify_token(token: str, secret: str, max_age: int = 3600) -> bool:
    try:
        user_id, timestamp, sig = token.split(".")
        if time.time() - int(timestamp) > max_age:
            return False
        expected = hmac.new(
            secret.encode(),
            f"{user_id}:{timestamp}".encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(sig, expected)
    except Exception:
        return False
````
=== END FILE: src/auth.py ===

=== BEGIN FILE: config/settings.json (json) ===
````json
{
  "service": "auth-service",
  "version": "1.0.0",
  "token_ttl_seconds": 3600,
  "algorithm": "HMAC-SHA256"
}
````
=== END FILE: config/settings.json ===

## Downstream Agent Ingestion Instructions
1. Parse all blocks bounded by `=== BEGIN FILE: <path> (<lang>) ===` and `=== END FILE: <path> ===`.
2. Extract the inner content verbatim (stripping the enclosing 4-backtick fence).
3. Create destination folders and write each file to its exact relative path.
4. Confirm the sentinel termination marker below before proceeding with execution.

=== END OF SPECIFICATION ===
