#!/usr/bin/env python3
"""
ASG Instance Poller for IT457 Hotstar Cloud Scaling PoC.
Logs InService instance count to results/raw/instances.csv every 10 seconds.

Features:
- Dual Mode:
  1. AWS Boto3 API Mode (if AWS credentials exist)
  2. Automatic Smart ALB Probing Mode (zero credentials needed! Samples ALB to detect distinct instance IDs)

Usage:
    python loadtest/poller.py [--url http://YOUR-ALB-URL] [--asg hotstar-asg] [--region ap-south-1]
"""

import argparse
import csv
import os
import sys
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError
except ImportError:
    boto3 = None


def run_alb_polling(url, out_path, interval=10):
    url = url.rstrip("/")
    probe_url = f"{url}/"
    print(f"[*] Running in Zero-Creds Smart ALB Probing Mode against: {probe_url}")
    print(f"[*] Writing to: {out_path}")
    print("[*] Press Ctrl+C to stop.\n")

    recent_instances = deque(maxlen=20)
    file_exists = out_path.exists() and out_path.stat().st_size > 0

    with open(out_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "iso_time", "in_service", "total", "detected_instances"])
            f.flush()

        while True:
            now = int(time.time())
            iso_now = datetime.now(timezone.utc).strftime("%H:%M:%S")
            seen_this_tick = set()

            # Send 4 quick probes to ALB to sample balanced targets
            for _ in range(4):
                try:
                    r = requests.get(probe_url, timeout=3)
                    if r.status_code == 200:
                        data = r.json()
                        inst_id = data.get("instance")
                        if inst_id:
                            seen_this_tick.add(inst_id)
                            recent_instances.append((now, inst_id))
                except Exception:
                    pass
                time.sleep(0.3)

            # Instances seen within the last 35 seconds
            active_recent = {iid for ts, iid in recent_instances if now - ts <= 35}
            active_count = max(1, len(active_recent))

            print(f"[{iso_now}] In-Service Instances: {active_count} | Active IDs: {list(active_recent)}")
            writer.writerow([now, datetime.now(timezone.utc).isoformat(), active_count, active_count, ";".join(active_recent)])
            f.flush()

            time.sleep(max(1, interval - 2))


def main():
    default_alb = os.environ.get("ALB_URL", "http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com")
    parser = argparse.ArgumentParser(description="Poll ASG instance count periodically.")
    parser.add_argument("--url", default=default_alb, help="ALB URL for zero-creds polling")
    parser.add_argument("--asg", default=os.environ.get("ASG_NAME", "hotstar-asg"), help="Auto Scaling Group name")
    parser.add_argument("--region", default=os.environ.get("AWS_REGION", "ap-south-1"), help="AWS Region (default: ap-south-1)")
    parser.add_argument("--interval", type=int, default=10, help="Polling interval in seconds")
    parser.add_argument("--out", default="results/raw/instances.csv", help="Output CSV path")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if Boto3 can authenticate
    use_boto = False
    if boto3 is not None:
        try:
            client = boto3.client("autoscaling", region_name=args.region)
            client.describe_auto_scaling_groups(AutoScalingGroupNames=[args.asg])
            use_boto = True
        except (NoCredentialsError, ClientError, BotoCoreError, Exception):
            use_boto = False

    if not use_boto:
        if requests is None:
            print("[!] Error: requests package required for ALB polling. Run 'pip install requests'.")
            sys.exit(1)
        try:
            run_alb_polling(args.url, out_path, args.interval)
        except KeyboardInterrupt:
            print("\n[*] Poller stopped. CSV saved successfully.")
        return

    # Boto3 mode
    print(f"[*] Starting AWS Boto3 Poller for group '{args.asg}' in '{args.region}'")
    print(f"[*] Writing to: {out_path}")
    print("[*] Press Ctrl+C to stop.\n")

    file_exists = out_path.exists() and out_path.stat().st_size > 0
    with open(out_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "iso_time", "in_service", "total"])
            f.flush()

        try:
            while True:
                now = int(time.time())
                iso_now = datetime.now(timezone.utc).strftime("%H:%M:%S")
                resp = client.describe_auto_scaling_groups(AutoScalingGroupNames=[args.asg])
                groups = resp.get("AutoScalingGroups", [])
                if groups:
                    instances = groups[0].get("Instances", [])
                    in_service = sum(1 for i in instances if i.get("LifecycleState") == "InService")
                    total = len(instances)
                    print(f"[{iso_now}] In-Service: {in_service} | Total: {total}")
                    writer.writerow([now, datetime.now(timezone.utc).isoformat(), in_service, total])
                    f.flush()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n[*] Poller stopped. CSV saved successfully.")


if __name__ == "__main__":
    main()
