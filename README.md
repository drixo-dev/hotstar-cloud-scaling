# Hotstar Cloud Scaling — High-Traffic Cricket Streaming PoC

**Course:** IT457 — Cloud Computing  
**Group:** 19 (Jill Chhagnani – 202301273, Dhyey Patel – 202301415, Jay Patel – 202301430)  
**Theme:** Theme 1: Scalability & High-Traffic Events (Hotstar, IRCTC, Flipkart)  
**Tech Stack:** Python 3.12, FastAPI, Uvicorn, Docker, AWS (ALB, EC2, ASG, CloudWatch), Locust, Matplotlib  

---

## 1. Project Overview

During major live cricket tournaments (such as the ICC Men's Cricket World Cup and IPL), streaming platforms like Disney+ Hotstar experience catastrophic traffic surges where millions of concurrent viewers join within seconds of match start or critical wickets (e.g. 6–8 million viewers in under 120 seconds). 

Standard reactive cloud autoscaling struggles because virtual machine provisioning takes 2–4 minutes (*scale-out lag*), causing request timeouts and cascading client retries before new servers boot.

This project implements an end-to-end **Cloud Proof of Concept (PoC)** on AWS to evaluate and demonstrate:
1. **Multi-AZ Application Load Balancer (ALB)** distributing incoming streaming traffic across healthy dynamic targets in `ap-south-1a` and `ap-south-1b`.
2. **Auto Scaling Group (ASG)** scaling out EC2 instances automatically when average **CPU utilization exceeds 50%**.
3. **Scale-Out Lag & Tail Latency Analysis**, measuring p50/p95/p99 response times vs. instance count under a simulated cricket traffic tsunami using **Locust**.
4. **Graceful Scale-In**, verifying connection draining (30-second deregistration delay) to prevent dropped in-flight requests.

---

## 2. Course Deliverables Status

| Deliverable | Requirement | Status | Evidence Location |
|:---|:---|:---:|:---|
| **Deliverable 1** | Live ALB URL returning a simple response | **100% Completed** | `http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com/` |
| **Deliverable 2** | ASG dashboard screenshots of automatic scaling (>50% CPU) | **100% Completed** | `results/screenshots/03_ASG_a.png`, `05_cloudwatch_50pct_alarm.png`, `06_EC2_inst_scale.png`, `07_EC2_tg.png` |
| **Deliverable 3** | Load testing report & plots: **Response Time vs. Instance Count** | **100% Completed** | `analysis/deliverable_plots/fig1_response_time_vs_instance_count.png`, `results/report.html` |
| **Scale-In Proof** | Graceful scale-in and connection draining after load drops | **100% Completed** | `results/screenshots/10_draining.png`, `11_draining_asg.png` |
| **Academic Reports** | Week 2 Case Study & Final Technical Report | **100% Completed** | `reports/IT457_Group19_Week2_Report.pdf`, `reports/IT457_Group19_Final_Report.pdf` |

---

## 3. High Availability Architecture (Dual Availability Zones)

The cloud infrastructure is provisioned inside a custom VPC (`10.50.0.0/16`) in AWS Mumbai (`ap-south-1`):
* **Subnet A (`10.50.0.0/24`):** Located in Availability Zone **`ap-south-1a`**.
* **Subnet B (`10.50.1.0/24`):** Located in Availability Zone **`ap-south-1b`**.
* **Ingress:** AWS Application Load Balancer spans both subnets for regional fault tolerance.
* **Auto Scaling Group:** Configured with `Balanced best effort` distribution, automatically maintaining a 50/50 instance split between `ap-south-1a` and `ap-south-1b` to survive a single data center outage.

---

## 4. Step-by-Step Deployment & Execution Guide

### 4.1 Prerequisites
* An AWS Account with permissions for VPC, EC2, Auto Scaling, ALB, CloudWatch, and IAM.
* Recommended AWS Region: **Asia Pacific (Mumbai) `ap-south-1`**.
* Local machine with Python 3.10+ installed.

---

### 4.2 Step 1: Deploy Infrastructure to AWS (CloudFormation)

The entire cloud infrastructure (VPC, Dual Subnets, Internet Gateway, Security Groups, ALB, Target Group, Launch Template, ASG, and CloudWatch Alarms) is defined in a single template: [`infra/hotstar-fastapi-cfn.yaml`](infra/hotstar-fastapi-cfn.yaml).

#### Option A: Deploy via AWS Web Console (Recommended)
1. Log in to the [AWS Management Console](https://console.aws.amazon.com/) and set your region to **Asia Pacific (Mumbai) `ap-south-1`** (top right).
2. Type **CloudFormation** in the search bar and click **CloudFormation**.
3. Click the orange **Create stack** button $\rightarrow$ select **With new resources (standard)**.
4. Under **Prerequisite - Prepare template**, select **Template is ready**.
5. Under **Specify template**, select **Upload a template file**.
6. Click **Choose file** and select `infra/hotstar-fastapi-cfn.yaml` from this repository.
7. Click **Next**.
8. In **Stack details**:
   * **Stack name:** `hotstar-scaling-poc`
   * **InstanceType:** `t3.micro` *(default, Free Tier eligible)*
   * **KeyName:** *(leave blank unless SSH access is needed)*
9. Click **Next** on Configure stack options (keep all defaults).
10. Scroll to the bottom of the Review page, check the acknowledgment box:  
    ☑ *"I acknowledge that AWS CloudFormation might create IAM resources with custom names."*
11. Click **Submit**.
12. Creation takes approximately **2.5 to 3 minutes**. Wait until stack status turns green: **`CREATE_COMPLETE`**.

#### Option B: Deploy via AWS CLI (Alternative)
```bash
aws cloudformation create-stack \
  --stack-name hotstar-scaling-poc \
  --template-body file://infra/hotstar-fastapi-cfn.yaml \
  --capabilities CAPABILITY_IAM \
  --region ap-south-1
```
Wait for completion:
```bash
aws cloudformation wait stack-create-complete \
  --stack-name hotstar-scaling-poc \
  --region ap-south-1
```

---

### 4.3 Step 2: Retrieve ALB URL & Verify Endpoints

1. In the AWS CloudFormation Console, click on your stack `hotstar-scaling-poc` $\rightarrow$ open the **Outputs** tab.
2. Copy the **`LoadBalancerUrl`** (e.g. `http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com/`).
3. *(Allow 60–90 seconds for the initial EC2 instance UserData to initialize and pass health checks).*
4. Test the live endpoints:

```bash
export ALB_URL="http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com"

# 1. Test Root Ingress
curl -s "$ALB_URL/"

# 2. Test Health Check
curl -s "$ALB_URL/health"

# 3. Test CPU Compute Endpoint (burns ~30ms CPU)
curl -s "$ALB_URL/work?n=300000"

# 4. Or run the automated smoke test script:
python loadtest/local_smoke_test.py "$ALB_URL"
```

*Expected Smoke Test Output:*
```text
[*] Testing Root Endpoint -> http://.../ ... SUCCESS [HTTP 200]
[*] Testing Health Check Endpoint -> http://.../health ... SUCCESS [HTTP 200]
[*] Testing CPU Work Endpoint -> http://.../work?n=300000 ... SUCCESS [HTTP 200]
[+] ALL SMOKE TESTS PASSED! API is ready for load testing.
```

---

### 4.4 Step 3: Run the Load Test & Demonstrate Elasticity

#### Setup Local Virtual Environment:
```bash
# Clone the repository
git clone https://github.com/DhyeyPatel15/hotstar-cloud-scaling.git
cd hotstar-cloud-scaling

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install testing dependencies
pip install -r requirements.txt
```

#### Demo Scenario 1: Fast 3-Minute Live Viva Demo (Recommended for Evaluation)
Spawns 60 users immediately (at 10/s) hitting `/work?n=300000`. Drives CPU past 70%, triggers the 50% CloudWatch alarm within 60s, scales ASG from 1 to 2 instances, and automatically stops after 3 minutes to demonstrate scale-in:
```bash
source .venv/bin/activate
locust -f loadtest/locustfile.py --headless -u 60 -r 10 --run-time 3m --host http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com
```

#### Demo Scenario 2: Full 13-Minute Match Benchmark (55,910 Requests)
Executes the full multi-stage cricket spike profile (Warm-up $\rightarrow$ Tsunami $\rightarrow$ Plateau $\rightarrow$ Drop $\rightarrow$ Tail) used to generate the report data:
```bash
source .venv/bin/activate
USE_SHAPE=1 locust -f loadtest/locustfile.py --headless --host http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com
```

#### Optional: Run Real-Time Telemetry Poller
In a separate terminal window, run the background poller to track in-service instance counts during the test:
```bash
source .venv/bin/activate
python loadtest/poller.py --host http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com
```

---

### 4.5 Step 4: Generate Deliverable Plots

Once testing logs are collected in `results/raw/`, generate the publication figures:
```bash
source .venv/bin/activate
python analysis/plot.py
```
Outputs generated:
* `analysis/deliverable_plots/fig1_response_time_vs_instance_count.png` (Deliverable Plot F1)
* `analysis/deliverable_plots/fig2_latency_and_instances_vs_time.png` (Deliverable Plot F2)

---

### 4.6 Step 5: Clean Teardown (Zero-Cost Guarantee)

To guarantee $0.00 spend once your evaluation is complete, delete the stack:
* **Via AWS Console:** Go to **CloudFormation** $\rightarrow$ select `hotstar-scaling-poc` $\rightarrow$ click **Delete**.
* **Via AWS CLI:**
  ```bash
  aws cloudformation delete-stack --stack-name hotstar-scaling-poc --region ap-south-1
  ```
All provisioned EC2 instances, Load Balancers, Target Groups, Security Groups, Subnets, and CloudWatch Alarms will be automatically deleted in ~2 minutes.

---

## 5. Real Experiment Findings (55,910 Requests on AWS ap-south-1)

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

## 6. Repository Structure

```text
hotstar-cloud-scaling/
├── app.py                             # FastAPI application (/, /health, /work?n=300000)
├── Dockerfile                         # Multi-worker Python 3.12 container definition
├── requirements.txt                   # Complete dependencies (FastAPI, Locust, Boto3, Matplotlib)
├── infra/
│   └── hotstar-fastapi-cfn.yaml       # 1-Click AWS CloudFormation template (Dual-AZ VPC, ALB, ASG, Alarms)
├── loadtest/
│   ├── locustfile.py                  # High-traffic spike shape scenario (Locust)
│   ├── poller.py                      # Real-time ASG instance count logger (Boto3 & ALB Probe)
│   └── local_smoke_test.py            # Local/Remote endpoint validation script
├── analysis/
│   ├── plot.py                        # Deliverable figure generator (Response Time vs. Instance Count)
│   └── deliverable_plots/             # High-res Deliverable Figures (F1 and F2)
├── docs/
│   ├── AWS_SETUP_GUIDE.md             # Detailed step-by-step AWS guide
│   ├── EVIDENCE_CHECKLIST.md          # Detailed evidence log and viva talking points
│   └── VIVA_PREPARATION_GUIDE.md      # Private team viva defense cheat sheet
├── results/
│   ├── raw/                           # Raw CSV logs (55,910 requests and ASG instance history)
│   ├── figures/                       # Generated F1 and F2 plots
│   ├── report.html                    # Interactive Locust HTML performance report
│   └── screenshots/                   # All 12 AWS Console evidence screenshots (ALB, ASG, CW, Scaling)
└── reports/
    ├── IT457_Group19_Week2_Report.pdf  # Week 2 Comprehensive Study & Architecture Analysis
    ├── IT457_Group19_Final_Report.pdf  # Final Technical Report (Weeks 1–4 Deliverables)
    ├── figures/                        # High-resolution System and PoC Architecture diagrams
    └── week-1-case-study.pdf           # Week 1 Research and Case Study Report
```

---

## 7. Pacing & Milestones

- [x] **Week 1:** Case study research and summary ([`reports/week-1-case-study.pdf`](reports/week-1-case-study.pdf)).
- [x] **Week 2:** Detailed architecture, problem analysis, system diagrams, and PoC plan ([`reports/IT457_Group19_Week2_Report.pdf`](reports/IT457_Group19_Week2_Report.pdf)).
- [x] **Week 3:** Cloud infrastructure build, high-traffic simulation, metrics collection, and deliverable plots.
- [x] **Week 4:** Final Technical Report assembly, evidence dossier, and submission ([`reports/IT457_Group19_Final_Report.pdf`](reports/IT457_Group19_Final_Report.pdf)).
- [ ] **Week 5:** Viva defense.
