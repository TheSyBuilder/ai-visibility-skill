#!/usr/bin/env python3
"""Validate manually annotated AI answers and summarize descriptive proportions."""

import argparse
import csv
import json
import math
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

GROUP_FIELDS = (
    "experiment_id", "phase", "platform", "surface", "model", "locale", "query_type"
)
METRICS = (
    "brand_mentioned", "brand_recommended", "owned_page_cited",
    "third_party_brand_cited", "offer_accurate"
)
REQUIRED = (
    "run_id", "experiment_id", "phase", "platform", "surface", "model", "locale",
    "prompt_id", "query_type", "recorded_at", "status", "offer_in_scope", *METRICS,
    "answer_artifact", "notes"
)


def load_rows(path):
    """Reject ambiguous records rather than silently treating missing data as zero."""
    rows, seen = [], set()
    with Path(path).open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        headers = reader.fieldnames or []
        missing = set(REQUIRED) - set(headers)
        if missing:
            raise ValueError("Missing columns: " + ", ".join(sorted(missing)))
        if len(headers) != len(set(headers)):
            raise ValueError("Duplicate column names")
        for number, raw in enumerate(reader, start=2):
            prefix = f"CSV row {number}: "
            if None in raw or any(value is None for value in raw.values()):
                raise ValueError(prefix + "column count does not match header")
            row = {key: value.strip() for key, value in raw.items()}
            for field in ("run_id", "prompt_id", "recorded_at", *GROUP_FIELDS):
                if not row[field]:
                    raise ValueError(prefix + f"{field} must be nonempty")
            if row["run_id"] in seen:
                raise ValueError(prefix + "duplicate run_id " + row["run_id"])
            seen.add(row["run_id"])
            for field, allowed in (
                ("phase", {"baseline", "followup"}),
                ("query_type", {"unbranded", "branded"}),
                ("status", {"ok", "error", "not_run"}),
            ):
                if row[field] not in allowed:
                    raise ValueError(prefix + f"invalid {field}: {row[field]}")
            try:
                timestamp = datetime.fromisoformat(row["recorded_at"].replace("Z", "+00:00"))
                if timestamp.tzinfo is None or timestamp.utcoffset() is None:
                    raise ValueError("timezone is required")
            except ValueError as error:
                raise ValueError(prefix + "recorded_at requires an ISO timestamp with timezone") from error
            if row["status"] == "ok":
                if row["offer_in_scope"] not in {"0", "1"}:
                    raise ValueError(prefix + "offer_in_scope must be 0 or 1")
                for field in METRICS:
                    if row[field] not in {"0", "1", ""}:
                        raise ValueError(prefix + f"invalid or missing {field}")
                if row["offer_in_scope"] == "0" and row["offer_accurate"]:
                    raise ValueError(prefix + "out-of-scope offer must have blank offer_accurate")
                unknown = [field for field in METRICS if not row[field]
                           and (field != "offer_accurate" or row["offer_in_scope"] == "1")]
                if unknown and not row["notes"]:
                    raise ValueError(prefix + "unknown metrics require explanatory notes")
                if not row["answer_artifact"]:
                    raise ValueError(prefix + "successful runs require answer_artifact")
                if row["brand_mentioned"] != "1" and (
                    row["brand_recommended"] == "1" or row["offer_accurate"] == "1"
                ):
                    raise ValueError(prefix + "recommendation/accurate offer requires a brand mention")
            else:
                if any(row[field] for field in (*METRICS, "offer_in_scope", "answer_artifact")):
                    raise ValueError(prefix + "unobserved runs require blank metrics and artifact")
                if not row["notes"]:
                    raise ValueError(prefix + "unobserved runs require explanatory notes")
            rows.append(row)
    return rows


def wilson(positive, total):
    if not total:
        return None
    z = 1.959963984540054
    p = positive / total
    scale = 1 + z * z / total
    center = (p + z * z / (2 * total)) / scale
    half = z * math.sqrt(p * (1 - p) / total + z * z / (4 * total * total)) / scale
    return [max(0.0, center - half), min(1.0, center + half)]


def summarize(rows):
    strata = defaultdict(list)
    for row in rows:
        strata[tuple(row[field] for field in GROUP_FIELDS)].append(row)
    groups = []
    for key, attempts in sorted(strata.items()):
        observed = [row for row in attempts if row["status"] == "ok"]
        counts = {status: sum(row["status"] == status for row in attempts)
                  for status in ("ok", "error", "not_run")}
        timestamps = sorted(datetime.fromisoformat(row["recorded_at"].replace("Z", "+00:00"))
                            .astimezone(timezone.utc).isoformat() for row in attempts)
        group = dict(zip(GROUP_FIELDS, key))
        group.update(
            planned_rows=len(attempts), status_counts=counts,
            collection_success_rate=len(observed) / len(attempts),
            prompt_ids=sorted({row["prompt_id"] for row in attempts}),
            observed_prompt_ids=sorted({row["prompt_id"] for row in observed}),
            observed_at_range_utc=[timestamps[0], timestamps[-1]],
        )
        metrics = {}
        for field in METRICS:
            applicable = [row for row in observed
                          if field != "offer_accurate" or row["offer_in_scope"] == "1"]
            measured = [row for row in applicable if row[field] != ""]
            unknown = len(applicable) - len(measured)
            positive = sum(int(row[field]) for row in measured)
            per_prompt = defaultdict(list)
            for row in measured:
                per_prompt[row["prompt_id"]].append(int(row[field]))
            prompt_rates = {prompt: {"positive": sum(values), "measured": len(values),
                                     "rate": sum(values) / len(values)}
                            for prompt, values in sorted(per_prompt.items())}
            metrics[field] = {
                "positive": positive, "measured": len(measured),
                "not_applicable": len(observed) - len(applicable),
                "unknown": unknown,
                "annotation_coverage": len(measured) / len(applicable) if applicable else None,
                "possible_rate_bounds": (
                    [positive / len(applicable), (positive + unknown) / len(applicable)]
                    if applicable else None
                ),
                "rate": positive / len(measured) if measured else None,
                "wilson_95_descriptive": wilson(positive, len(measured)),
                "equal_prompt_mean": (
                    sum(item["rate"] for item in prompt_rates.values()) / len(prompt_rates)
                    if prompt_rates else None
                ),
                "per_prompt": prompt_rates,
            }
        group["metrics"] = metrics
        groups.append(group)
    return {
        "schema_version": 1,
        "measurement_status": "observed" if any(r["status"] == "ok" for r in rows) else "unmeasured",
        "total_planned_rows": len(rows),
        "notes": [
            "Only supplied planned rows are counted; absent schedule rows cannot be detected.",
            "Intervals are descriptive: repeated prompts and dates may be correlated.",
            "Check identical prompt coverage and experimental conditions before comparing phases.",
            "Artifacts and annotations are not independently verified by this helper.",
        ],
        "groups": groups,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="CSV following references/measurement.md")
    parser.add_argument("--output", type=Path, help="Write JSON here instead of stdout")
    args = parser.parse_args(argv)
    if args.output and args.output.resolve() == args.input.resolve():
        parser.error("output must differ from input")
    try:
        result = summarize(load_rows(args.input))
        encoded = json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
        if args.output:
            args.output.write_text(encoded, encoding="utf-8")
        else:
            sys.stdout.write(encoded)
    except (OSError, ValueError, csv.Error) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
