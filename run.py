#!/usr/bin/env python3
"""
Trigger script: runs the buggy code in app.py, catches the exception,
and POSTs error_class, message, and stack_trace to Oopsie at POST /api/v1/errors.
"""
import json
import os
import traceback
import urllib.error
import urllib.request

from dotenv import load_dotenv

load_dotenv()


def report_to_oopsie(error_class: str, message: str, stack_trace: str) -> None:
    """POST the error payload to Oopsie."""
    api_url = os.environ.get("OOPSIE_API_URL", "http://localhost:8000").rstrip("/")
    api_key = os.environ.get("OOPSIE_API_KEY")
    if not api_key:
        raise SystemExit("OOPSIE_API_KEY environment variable is required")

    url = f"{api_url}/api/v1/errors"
    payload = {
        "error_class": error_class,
        "message": message,
        "stack_trace": stack_trace,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status in (200, 201, 204):
                print("Error reported to Oopsie.")
            else:
                print(f"Unexpected response: {resp.status} {resp.read()}")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Oopsie API error: {e.code} {e.reason}\n{body}")
    except urllib.error.URLError as e:
        raise SystemExit(f"Could not reach Oopsie: {e.reason}")


def main() -> None:
    from app import process_input

    try:
        process_input(None)  # Triggers the bug every run
    except Exception as exc:
        report_to_oopsie(
            error_class=type(exc).__name__,
            message=str(exc),
            stack_trace=traceback.format_exc(),
        )
        raise


if __name__ == "__main__":
    main()
