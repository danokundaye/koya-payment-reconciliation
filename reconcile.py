#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json

total = 0.0
count = 0
latest_payments = {}

with open("payments.jsonl") as f:
    for line in f:
        try:
            event = json.loads(line)
            if "txn_id" not in event or not event["txn_id"]:
                continue
            current_id = event["txn_id"]
            if current_id not in latest_payments:
                latest_payments[current_id] = event
            else:
                if event["ts"] > latest_payments[current_id]["ts"]:
                    latest_payments[current_id] = event
        except (json.JSONDecodeError, KeyError, ValueError):
            # Skip lines that are not valid JSON or don't have the expected structure
            continue
    for item in latest_payments.values():
        if item["status"] == "success":
            total += float(str(item["amount"]).replace(",", ""))
            count += 1

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
