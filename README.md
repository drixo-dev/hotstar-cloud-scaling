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

## 2. Course Deliverables Status

| Deliverable | Requirement | Status | Evidence Location |
|:---|:---|:---:|:---|
| **Deliverable 1** | Live ALB URL returning a simple response | **100% Completed** | `http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com/` |
| **Deliverable 2** | ASG dashboard screenshots of automatic scaling (>50% CPU) | **100% Completed** | `results/screenshots/05_cloudwatch_50pct_alarm.png`, `06_EC2_inst_scale.png`, `07_EC2_tg.png` |
| **Deliverable 3** | Load testing report & plot: **Response Time vs. Instance Count** | **100% Completed** | `results/figures/F2_response_time_vs_instance_count.png`, `results/report.html` |
| **Scale-In Proof** | Graceful scale-in and connection draining after load drops | **100% Completed** | `results/screenshots/10_draining.png`, `11_draining_asg.png` |

---

## 3. Real Experiment Findings (55,910 Requests on AWS ap-south-1)

Under a 13-minute cricket match traffic spike executed against the live AWS Application Load Balancer:

| In-Service Instances | Median p50 Latency (ms) | Median p95 Latency (ms) | Observation |
|:---:|:---:|:---:|:---|
| **1 Instance** | 590.0 ms | 1,200.0 ms | Initial baseline before the full spike hit. |
| **2 Instances** | 930.0 ms | 2,100.0 ms | **Scale-Out Lag:** Peak traffic hit while new VMs were booting. |
| **3 Instances** | 480.0 ms | 1,400.0 ms | Third server joined; latency started dropping rapidly. |
| **4 Instances** | **73.0 ms** | **330.0 ms** | **Cluster Stabilized:** Full capacity absorbed traffic (**84% drop in p95 latency**). |

* **Total Requests Handled:** 55,910
* **Success Rate:** 99.58% (only 0.42% transient timeouts during initial 2-minute instance boot lag)
* **Scale-In:** Scaled down smoothly from 4 instances to 1 instance after traffic stopped.
* **Cost:** $0.00 (100% covered under AWS Free Tier).

---

## 4. Repository Structure

```text
hotstar-cloud-scaling/
├── app.py                     # FastAPI application (/, /health, /work?n=300000)
├── Dockerfile                 # Multi-worker Python 3.12-slim container definition
├── requirements.txt           # App dependencies (FastAPI, Uvicorn)
├── infra/
│   └── hotstar-fastapi-cfn.yaml  # 1-Click AWS CloudFormation template (VPC, ALB, ASG, Alarms)
├── loadtest/
│   ├── locustfile.py          # High-traffic spike shape scenario (Locust)
│   ├── poller.py              # Real-time ASG instance count logger (Boto3 & ALB Probe)
│   └── local_smoke_test.py    # Local/Remote endpoint validation script
├── analysis/
│   └── plot.py                # Deliverable figure generator (Response Time vs. Instance Count)
├── docs/
│   ├── AWS_SETUP_GUIDE.md     # Complete step-by-step AWS guide (Zero-Cost / Free Tier)
│   └── EVIDENCE_CHECKLIST.md  # Detailed evidence log and viva talking points
├── results/
│   ├── raw/                   # Raw CSV logs (55k requests and ASG instance history)
│   ├── figures/               # Generated F1 and F2 (Response Time vs Instance Count) plots
│   ├── report.html            # Interactive Locust HTML performance report
│   └── screenshots/           # All 11 required AWS Console evidence screenshots
└── reports/
    └── week-1-case-study.pdf  # Week 1 Research and Case Study Report
```

---

## 5. Pacing & Milestones

- [x] **Week 1:** Case study research and summary ([`reports/week-1-case-study.pdf`](reports/week-1-case-study.pdf)).
- [x] **Week 2:** Detailed architecture, problem analysis, solution design, and team roles.
- [x] **Week 3:** Cloud infrastructure build, high-traffic simulation, metrics collection, and deliverable plots.
- [ ] **Week 4:** Final written report assembly and submission.
- [ ] **Week 5:** Viva defense.

---

## 6. Teardown (Zero-Billing Guarantee)

To ensure zero charges within AWS Free Tier once evaluation is finished:
1. Go to **CloudFormation** $\rightarrow$ Select `hotstar-scaling-poc` $\rightarrow$ Click **Delete**.
2. All resources (ALB, ASG, EC2 instances, Security Groups, Subnets, VPC) will be automatically removed in ~2 minutes.
