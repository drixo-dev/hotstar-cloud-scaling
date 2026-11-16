#!/usr/bin/env python3
"""
ASG Instance Poller for IT457 Hotstar Cloud Scaling PoC.
Logs InService and Total instance count from AWS Auto Scaling Group every 10 seconds.

Usage:
    python loadtest/poller.py [--asg hotstar-asg] [--region ap-south-1] [--out results/raw/instances.csv]
"""

import argparse
import csv
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import boto3
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    print("Error: boto3 is not installed. Run 'pip install boto3' in your virtual environment.")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Poll ASG instance count periodically.")
    parser.add_argument("--asg", default=os.environ.get("ASG_NAME", "hotstar-asg"), help="Auto Scaling Group name")
    parser.add_argument("--region", default=os.environ.get("AWS_REGION", "ap-south-1"), help="AWS Region (default: ap-south-1)")
    parser.add_argument("--interval", type=int, default=10, help="Polling interval in seconds (default: 10)")
    parser.add_argument("--out", default="results/raw/instances.csv", help="Output CSV path")
    args = parser.parse_args()

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        asg_client = boto3.client("autoscaling", region_name=args.region)
    except Exception as e:
        print(f"Failed to initialize boto3 client: {e}")
        sys.exit(1)

    print(f"[*] Starting ASG poller for group '{args.asg}' in region '{args.region}'")
    print(f"[*] Writing to: {out_path}")
    print("[*] Press Ctrl+C to stop.")

    file_exists = out_path.exists() and out_path.stat().st_size > 0

    with open(out_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "iso_time", "in_service", "pending", "terminating", "total"])
            f.flush()

        try:
            while True:
                now = int(time.time())
                iso_now = datetime.now(timezone.utc).isoformat()
                try:
                    response = asg_client.describe_auto_scaling_groups(
                        AutoScalingGroupNames=[args.asg]
                    )
                    groups = response.get("AutoScalingGroups", [])
                    if not groups:
                        print(f"[{iso_now}] Warning: ASG '{args.asg}' not found in region '{args.region}'.")
                        writer.writerow([now, iso_now, 0, 0, 0, 0])
                    else:
                        instances = groups[0].get("Instances", [])
                        in_service = sum(1 for i in instances if i.get("LifecycleState") == "InService")
                        pending = sum(1 for i in instances if "Pending" in i.get("LifecycleState", ""))
                        terminating = sum(1 for i in instances if "Terminating" in i.get("LifecycleState", ""))
                        total = len(instances)

                        print(f"[{iso_now}] Instances: {in_service} InService, {pending} Pending, {total} Total")
                        writer.writerow([now, iso_now, in_service, pending, terminating, total])
                    f.flush()
                except (BotoCoreError, ClientError) as aws_err:
                    print(f"[{iso_now}] AWS Error: {aws_err}")
                except Exception as ex:
                    print(f"[{iso_now}] Unexpected Error: {ex}")

                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\n[*] Polling stopped by user. CSV saved.")


if __name__ == "__main__":
    main()
