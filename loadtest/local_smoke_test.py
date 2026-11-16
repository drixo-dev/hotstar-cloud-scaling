#!/usr/bin/env python3
"""
Local Smoke Test for FastAPI Hotstar PoC.
Verifies that endpoints /, /health, and /work return expected JSON and status codes.
"""

import sys
import time
import requests


def test_endpoint(url, name):
    print(f"[*] Testing {name} -> {url} ...", end=" ")
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            print(f"SUCCESS [HTTP 200] -> {r.json()}")
            return True
        else:
            print(f"FAILED [HTTP {r.status_code}]")
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    base_url = base_url.rstrip("/")

    print("=" * 60)
    print(f"  HOTSTAR POC SMOKE TEST: {base_url}")
    print("=" * 60)

    t1 = test_endpoint(f"{base_url}/", "Root Endpoint")
    t2 = test_endpoint(f"{base_url}/health", "Health Check Endpoint")
    t3 = test_endpoint(f"{base_url}/work?n=300000", "CPU Work Endpoint")

    if t1 and t2 and t3:
        print("\n[+] ALL SMOKE TESTS PASSED! API is ready for load testing.")
        sys.exit(0)
    else:
        print("\n[!] SMOKE TESTS FAILED. Check server logs.")
        sys.exit(1)


if __name__ == "__main__":
    main()
