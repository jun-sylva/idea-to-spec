#!/usr/bin/env python3
"""Derive workflow metrics from an append-only Idea to Spec event log."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def moment(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def derive(payload: dict) -> dict:
    events = sorted(payload.get("events", []), key=lambda item: item.get("occurred_at", ""))
    starts, cycles, pending, cr, debt = {}, {}, {}, {}, set()
    debt_opened = debt_resolved = 0
    scope_added = scope_removed = 0
    notes = []
    for event in events:
        kind, data = event.get("type"), event.get("data", {})
        key = (event.get("phase"), event.get("version"))
        try:
            when = moment(event["occurred_at"])
        except (KeyError, TypeError, ValueError):
            notes.append(f"Horodatage invalide : {event.get('event_id')}")
            continue
        if kind == "PHASE_STARTED":
            starts[key] = when
        elif kind == "PHASE_COMPLETED" and key in starts:
            cycles[f"{key[0]}@{key[1]}"] = round((when - starts[key]).total_seconds() / 3600, 2)
        elif kind == "APPROVAL_REQUESTED":
            pending[data.get("approval_id", event.get("event_id"))] = event.get("occurred_at")
        elif kind in {"APPROVAL_DECIDED", "APPROVAL_REVOKED"}:
            pending.pop(data.get("approval_id"), None)
        elif kind == "CR_OPENED":
            cr[data.get("cr_id", event.get("event_id"))] = "OPEN"
        elif kind == "CR_DECIDED":
            cr[data.get("cr_id", event.get("event_id"))] = data.get("decision", "DECIDED")
        elif kind == "SCOPE_CHANGED":
            scope_added += int(data.get("requirements_added", 0))
            scope_removed += int(data.get("requirements_removed", 0))
        elif kind == "SPEC_DEBT_OPENED":
            debt.add(data.get("debt_id", event.get("event_id")))
            debt_opened += 1
        elif kind == "SPEC_DEBT_RESOLVED":
            debt.discard(data.get("debt_id"))
            debt_resolved += 1
    dates = [event.get("occurred_at") for event in events if event.get("occurred_at")]
    period_end = max(dates) if dates else None
    pending_rows = []
    for key, value in sorted(pending.items()):
        row = {"approval_id": key, "requested_at": value, "age_hours_at_period_end": None}
        if period_end:
            try:
                row["age_hours_at_period_end"] = round((moment(period_end) - moment(value)).total_seconds() / 3600, 2)
            except ValueError:
                notes.append(f"Date de demande invalide : {key}")
        pending_rows.append(row)
    return {"schema_version": "1.0", "project": payload.get("project"), "period": {"from": min(dates) if dates else None, "to": period_end}, "event_count": len(events), "pending_approvals": pending_rows, "cycle_times_hours": cycles, "change_requests": cr, "scope_change": {"requirements_added": scope_added, "requirements_removed": scope_removed}, "spec_debt": {"opened": debt_opened, "resolved": debt_resolved, "currently_open": len(debt), "open_ids": sorted(debt)}, "data_quality_notes": notes}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events", type=Path)
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.events.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False))
        return 1
    if payload.get("schema_version") != "1.0" or not isinstance(payload.get("events"), list):
        print(json.dumps({"error": "invalid_event_log"}, ensure_ascii=False))
        return 1
    print(json.dumps(derive(payload), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
