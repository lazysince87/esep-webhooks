"""Forward GitHub issue events for the assignment repository to Slack."""

import json
import os
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen


ISSUE_URL = re.compile(
    r"https://github\.com/lazysince87/esep-webhooks/issues/[1-9][0-9]*"
)


def lambda_handler(event, _context):
    """Receive the raw JSON body from the API Gateway REST integration."""
    issue = event.get("issue") if isinstance(event, dict) else None
    issue_url = issue.get("html_url") if isinstance(issue, dict) else None
    if not isinstance(issue_url, str) or not ISSUE_URL.fullmatch(issue_url):
        return "ignored"

    slack_url = os.environ.get("SLACK_URL", "").strip()
    if not slack_url:
        raise RuntimeError("Set SLACK_URL in the Lambda environment variables.")

    payload = json.dumps({"text": f"Issue Created: {issue_url}"}).encode("utf-8")
    try:
        request = Request(
            slack_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=4) as response:
            if response.read(64).strip() != b"ok":
                raise RuntimeError("Slack did not acknowledge the message.")
    except HTTPError as error:
        raise RuntimeError(f"Slack rejected the request (HTTP {error.code}).") from None
    except (OSError, ValueError):
        raise RuntimeError("Could not reach the Slack webhook.") from None

    return "ok"
