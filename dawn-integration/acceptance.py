#!/usr/bin/env python3
"""Secret-free offline acceptance for the DAWN AutoClip boundary.

This validator does not read or process media. It only proves that a proposed
first canary is local, authorised, rights-cleared and bounded.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ALLOWED_STYLES = {"clean_lower", "boxed", "bold_pop", "karaoke_fill"}


def validate(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if payload.get("schema_version") != 1:
        errors.append("schema_version")
    if payload.get("authorised") is not True:
        errors.append("operator_authority_required")
    if payload.get("source_type") != "local_file":
        errors.append("local_file_only")
    source_path = payload.get("source_path")
    if not isinstance(source_path, str) or not source_path.startswith("/"):
        errors.append("absolute_source_path_required")
    elif "://" in source_path:
        errors.append("remote_source_prohibited")
    if payload.get("source_owned_or_licensed") is not True:
        errors.append("media_rights_required")
    if payload.get("network_execution") is not False:
        errors.append("network_execution_prohibited")
    if payload.get("model_route") != "local_ollama":
        errors.append("local_ollama_required")
    if payload.get("provider_credentials") is not False:
        errors.append("provider_credentials_prohibited")
    if payload.get("direct_publish") is not False:
        errors.append("direct_publish_prohibited")
    if payload.get("social_credentials") is not False:
        errors.append("social_credentials_prohibited")
    if payload.get("diarisation_download") is not False:
        errors.append("diarisation_download_prohibited")
    if payload.get("output_destination") != "canary_only":
        errors.append("canary_output_only")
    if payload.get("aspect_ratio") != "9:16":
        errors.append("first_canary_aspect_ratio")
    if payload.get("caption_style") not in ALLOWED_STYLES:
        errors.append("caption_style")
    duration = payload.get("max_source_duration_seconds")
    if not isinstance(duration, int) or not 1 <= duration <= 600:
        errors.append("source_duration_limit")
    max_clips = payload.get("max_clips")
    if not isinstance(max_clips, int) or not 1 <= max_clips <= 3:
        errors.append("clip_count_limit")
    output_dir = payload.get("output_dir")
    if not isinstance(output_dir, str) or not output_dir.startswith("/"):
        errors.append("absolute_output_dir_required")
    return errors


def evaluate(payload: dict[str, Any]) -> dict[str, Any]:
    errors = validate(payload)
    return {
        "schema_version": 1,
        "capability": "dawn-autoclip",
        "operation": "validate-local-media-canary",
        "status": "blocked" if errors else "success",
        "data": {
            "canary_eligible": not errors,
            "media_processed": False,
            "model_called": False,
            "service_started": False,
            "asset_published": False,
        },
        "warnings": errors,
        "network_used": False,
        "credentials_used": False,
        "external_actions_performed": False,
    }


def main() -> int:
    valid = json.loads((ROOT / "fixtures" / "valid-canary.json").read_text())
    invalid = json.loads((ROOT / "fixtures" / "invalid-canary.json").read_text())
    accepted = evaluate(valid)
    refused = evaluate(invalid)
    assertions = [
        accepted["status"] == "success",
        accepted["data"]["media_processed"] is False,
        accepted["data"]["model_called"] is False,
        accepted["data"]["asset_published"] is False,
        accepted["external_actions_performed"] is False,
        refused["status"] == "blocked",
        "local_file_only" in refused["warnings"],
        "media_rights_required" in refused["warnings"],
        "network_execution_prohibited" in refused["warnings"],
        "direct_publish_prohibited" in refused["warnings"],
        "clip_count_limit" in refused["warnings"],
    ]
    report = {
        "capability": "dawn-autoclip",
        "status": "passed" if all(assertions) else "failed",
        "tests": len(assertions),
        "passed": sum(assertions),
        "network_used": False,
        "credentials_required": False,
        "media_processed": False,
        "external_actions_performed": False,
    }
    print(json.dumps(report, indent=2))
    return 0 if all(assertions) else 1


if __name__ == "__main__":
    sys.exit(main())
