# Hotstar Cloud Scaling — High-Traffic Cricket Streaming PoC

**Course:** IT457 — Cloud Computing  
**Group:** 19 (Jill Chhagnani – 202301273, Dhyey Patel – 202301415, Jay Patel – 202301430)  
**Theme:** Theme 1: Scalability & High-Traffic Events (Hotstar, IRCTC, Flipkart)  
**Tech Stack:** Python 3.12, FastAPI, Uvicorn, Docker, AWS (ALB, EC2, ASG, CloudWatch), Locust, Matplotlib

---

## 1. Project Overview

During major live cricket tournaments (such as the ICC World Cup and IPL), streaming platforms like Hotstar experience catastrophic traffic surges where millions of viewers join within seconds of match start or critical wickets. 

This project implements an end-to-end **Cloud Proof of Concept (PoC)** to evaluate:
1. **Application Load Balancer (ALB)** distributing incoming streaming traffic across dynamic targets.
2. **Auto Scaling Group (ASG)** scaling out EC2 instances automatically when average **CPU utilization exceeds 50%**.
3. **Scale-out lag & performance analysis**, measuring p50/p95 response time vs. instance count under a simulated cricket traffic tsunami using **Locust**.

---

## 2. Repository Structure

```text
hotstar-cloud-scaling/
├── app.py                     # FastAPI application (/, /health, /work?n=300000)
├── Dockerfile                 # Multi-worker Python 3.12-slim container definition
├── requirements.txt           # App dependencies (FastAPI, Uvicorn)
├── infra/
│   └── hotstar-fastapi-cfn.yaml  # 1-Click AWS CloudFormation template (VPC, ALB, ASG, Alarms)
├── loadtest/
│   ├── locustfile.py          # High-traffic spike shape scenario (Locust)
│   ├── poller.py              # Real-time ASG instance count logger (Boto3)
│   └── local_smoke_test.py    # Local/Remote endpoint validation script
├── analysis/
│   └── plot.py                # Deliverable figure generator (Response Time vs. Instance Count)
├── docs/
│   ├── AWS_SETUP_GUIDE.md     # Complete step-by-step AWS guide (Zero-Cost / Free Tier)
│   └── EVIDENCE_CHECKLIST.md  # Viva defense & submission screenshot checklist
├── results/
│   ├── raw/                   # Raw CSV logs from Locust and ASG poller
│   ├── figures/               # Generated F1 and F2 (Response Time vs Instance Count) plots
│   └── screenshots/           # Required AWS Console evidence screenshots
└── reports/
    └── week-1-case-study.pdf  # Week 1 Research and Case Study Report
```

---

## 3. Fast Setup & Execution

### A. Local Validation
```bash
# 1. Activate Python virtual environment
source .venv/bin/activate

# 2. Run local FastAPI server
uvicorn app:app --port 8000 --workers 2

# 3. In another terminal, run smoke test
python loadtest/local_smoke_test.py http://localhost:8000
```

### B. AWS Cloud Deployment (3 Minutes via CloudFormation)
1. Log in to [AWS Console](https://console.aws.amazon.com/) $\rightarrow$ select region **`ap-south-1` (Mumbai)**.
2. Go to **CloudFormation** $\rightarrow$ **Create stack** (with new resources).
3. Upload [`infra/hotstar-fastapi-cfn.yaml`](infra/hotstar-fastapi-cfn.yaml).
4. Click **Next** $\rightarrow$ Stack name: `hotstar-scaling-poc` $\rightarrow$ acknowledge IAM $\rightarrow$ **Submit**.
5. Once status is `CREATE_COMPLETE`, copy the `LoadBalancerUrl` from the **Outputs** tab.

*For complete click-by-click screenshots and instructions, refer to [AWS_SETUP_GUIDE.md](docs/AWS_SETUP_GUIDE.md).*

### C. Run the Load Test & Collect Metrics
```bash
# Terminal 1: Track ASG instances
python loadtest/poller.py --asg hotstar-asg --region ap-south-1

# Terminal 2: Run headless Locust against your live ALB URL
export ALB_URL="http://YOUR-ALB-DNS-NAME"
locust -f loadtest/locustfile.py --headless --host $ALB_URL --csv results/raw/locust --csv-full-history --html results/report.html
```

### D. Generate Deliverable Figures
```bash
python analysis/plot.py \
  --locust results/raw/locust_stats_history.csv \
  --instances results/raw/instances.csv \
  --out results/figures
```
This produces `results/figures/F2_response_time_vs_instance_count.png` (**Course Mandatory Deliverable**).

---

## 4. Teardown (Zero-Billing Guarantee)

To ensure zero charges within AWS Free Tier:
1. Go to **CloudFormation** $\rightarrow$ Select `hotstar-scaling-poc` $\rightarrow$ Click **Delete**.
2. All resources (ALB, ASG, EC2, VPC, Subnets) will be automatically removed.
