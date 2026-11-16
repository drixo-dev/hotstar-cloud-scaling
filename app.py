import os
import socket
import time
from fastapi import FastAPI, Query

app = FastAPI(
    title="Hotstar Cloud Scaling PoC",
    description="IT457 Proof of Concept API simulating high-traffic cricket streaming workloads.",
    version="1.0.0"
)

# Fetch instance hostname / ID so we can verify load balancing across instances
INSTANCE_ID = os.environ.get("INSTANCE_ID", socket.gethostname())


@app.get("/")
def root():
    """Root endpoint: confirms service is online and reports responding instance."""
    return {
        "status": "Stream available",
        "service": "hotstar-cloud-scaling-poc",
        "instance": INSTANCE_ID
    }


@app.get("/health")
def health():
    """Health check endpoint used by AWS Application Load Balancer Target Group."""
    return {
        "ok": True,
        "status": "healthy",
        "instance": INSTANCE_ID
    }


@app.get("/work")
def work(n: int = Query(default=300000, description="Number of CPU burn iterations")):
    """
    CPU-intensive arithmetic endpoint.
    Under concurrent requests, this burns CPU to push instance utilization above 50%,
    triggering the CloudWatch Alarm and Auto Scaling Group scale-out policy.
    """
    start = time.perf_counter()
    x = 0
    for i in range(n):
        x += i * i
    elapsed_ms = round((time.perf_counter() - start) * 1000, 2)
    return {
        "status": "Stream available",
        "n": n,
        "ms": elapsed_ms,
        "instance": INSTANCE_ID
    }