# AWS Complete Setup & Execution Guide (Free Tier / Zero-Cost)

**Course:** IT457 Cloud Computing  
**Project:** Hotstar Cloud Scaling Proof of Concept  
**Architecture:** Python FastAPI + AWS Application Load Balancer + EC2 Auto Scaling Group + CloudWatch 50% CPU Alarms

This guide takes you step-by-step from a **brand new AWS account** to running your live proof of concept, collecting required screenshots, generating your deliverable plots, and cleanly tearing down resources within **AWS Free Tier**.

---

## Table of Contents
1. [Prerequisites & Zero-Cost Guardrails](#1-prerequisites--zero-cost-guardrails)
2. [Step 1: Choose Your AWS Region](#step-1-choose-your-aws-region)
3. [Step 2: Fast-Track 3-Minute Deployment (CloudFormation)](#step-2-fast-track-3-minute-deployment-cloudformation)
4. [Step 3: Verify the Live Load Balancer URL](#step-3-verify-the-live-load-balancer-url)
5. [Step 4: Run the Locust High-Traffic Spike Test](#step-4-run-the-locust-high-traffic-spike-test)
6. [Step 5: Capture the 8 Required Evidence Screenshots](#step-5-capture-the-8-required-evidence-screenshots)
7. [Step 6: Generate the Required Figures (Python Analysis)](#step-6-generate-the-required-figures-python-analysis)
8. [Step 7: 1-Click Clean Teardown (Zero Billing Guarantee)](#step-7-1-click-clean-teardown-zero-billing-guarantee)
9. [Viva Defense: Manual Architecture Breakdown](#viva-defense-manual-architecture-breakdown)

---

## 1. Prerequisites & Zero-Cost Guardrails

### Free Tier Eligibility
* **EC2 `t3.micro` / `t2.micro`:** 750 hours/month free for 12 months on new AWS accounts.
* **Application Load Balancer (ALB):** 750 hours/month free for 12 months.
* **Auto Scaling & CloudWatch Basic Metrics:** Free of charge.
* Running this entire test session for 1–2 hours costs **$0.00**.

### Set Up a $1.00 Budget Alert (Protects your card)
1. In the top AWS search bar, type **Budgets** and click **AWS Budgets**.
2. Click **Create budget** $\rightarrow$ select **Zero spend budget** (or **Cost budget** set to `$1.00`).
3. Enter your email address to receive an alert if charges ever exceed $1.00.
4. Click **Create budget**.

---

## 2. Step 1: Choose Your AWS Region

In the top-right navbar of the AWS Management Console:
* Select **Asia Pacific (Mumbai) `ap-south-1`** (or **US East (N. Virginia) `us-east-1`**).
* **Important:** Keep this same region selected for all steps!

---

## 3. Step 2: Fast-Track 3-Minute Deployment (CloudFormation)

Instead of manually configuring 35+ settings across VPC, subnets, route tables, security groups, target groups, launch templates, and alarms, use the pre-built template [`infra/hotstar-fastapi-cfn.yaml`](file:///home/drixo/Projects/hotstar-cloud-scaling/infra/hotstar-fastapi-cfn.yaml).

### Steps in AWS Console:
1. Type **CloudFormation** in the top search bar and click it.
2. Click the orange **Create stack** button $\rightarrow$ select **With new resources (standard)**.
3. Under **Prerequisite - Prepare template**, select **Template is ready**.
4. Under **Specify template**, select **Upload a template file**.
5. Click **Choose file** and select:
   `/home/drixo/Projects/hotstar-cloud-scaling/infra/hotstar-fastapi-cfn.yaml`
6. Click **Next**.
7. In **Stack details**:
   * **Stack name:** `hotstar-scaling-poc`
   * **InstanceType:** `t3.micro` (default, Free Tier eligible)
   * **KeyName:** *(leave blank unless you want SSH access)*
8. Click **Next** on Configure stack options (keep all defaults).
9. Scroll to the bottom of the Review page. Check the acknowledgement box:  
   ☑ *"I acknowledge that AWS CloudFormation might create IAM resources with custom names."*
10. Click **Submit**.

CloudFormation will now automatically provision the VPC, Subnets, Internet Gateway, Security Groups, ALB, Target Group, EC2 Launch Template with Python FastAPI UserData, Auto Scaling Group, and CloudWatch Alarms.

> [!NOTE]
> Creation takes approximately **2.5 to 3 minutes**. Wait until the stack status turns green: **`CREATE_COMPLETE`**.

---

## 4. Step 3: Verify the Live Load Balancer URL

1. In the CloudFormation console, click on your stack `hotstar-scaling-poc`.
2. Click the **Outputs** tab.
3. Copy the **`LoadBalancerUrl`** (e.g. `http://hotstar-alb-123456789.ap-south-1.elb.amazonaws.com/`).
4. Wait 1–2 minutes for the initial EC2 instance to complete booting and pass health checks.
5. Test the URL from your laptop terminal:
   ```bash
   # Substitute your actual ALB URL (without trailing slash)
   export ALB_URL="http://YOUR-ALB-DNS-NAME"

   python loadtest/local_smoke_test.py $ALB_URL
   ```
   *Expected Output:*
   ```text
   [*] Testing Root Endpoint -> http://.../ ... SUCCESS [HTTP 200]
   [*] Testing Health Check Endpoint -> http://.../health ... SUCCESS [HTTP 200]
   [*] Testing CPU Work Endpoint -> http://.../work?n=300000 ... SUCCESS [HTTP 200]
   [+] ALL SMOKE TESTS PASSED! API is ready for load testing.
   ```
6. **Capture Evidence:**
   * Open `$ALB_URL` in your browser.
   * Screenshot the JSON response for your report (**Screenshot 1**).
   * Open the EC2 Console $\rightarrow$ **Target Groups** $\rightarrow$ `hotstar-tg` $\rightarrow$ **Targets** tab.
   * Verify 1 instance is listed with Health status **`Healthy`** (**Screenshot 2**).

---

## 5. Step 4: Run the Locust High-Traffic Spike Test

The load test replicates the Hotstar cricket match spike scenario using our Python script [`loadtest/locustfile.py`](file:///home/drixo/Projects/hotstar-cloud-scaling/loadtest/locustfile.py):
* **0–2 min:** 20 users (steady baseline)
* **2–3 min:** Rapid ramp to 150 users (spike)
* **3–10 min:** 150 users sustained (CPU > 50% causes ASG to scale out from 1 to 2+ instances)
* **10–12 min:** Drop back to 20 users (traffic cools down)
* **12–13 min:** Tail

### Running the Test (Open 2 Terminals):

#### Terminal 1: Start the ASG Instance Poller
```bash
cd /home/drixo/Projects/hotstar-cloud-scaling
source .venv/bin/activate

# Start logging ASG instance count every 10 seconds
python loadtest/poller.py --asg hotstar-asg --region ap-south-1
```
*Leave this running throughout the test.*

#### Terminal 2: Run Headless Locust
```bash
cd /home/drixo/Projects/hotstar-cloud-scaling
source .venv/bin/activate

export ALB_URL="http://YOUR-ALB-DNS-NAME"

locust -f loadtest/locustfile.py \
  --headless \
  --host $ALB_URL \
  --csv results/raw/locust \
  --csv-full-history \
  --html results/report.html
```

---

## 6. Step 5: Capture the 8 Required Evidence Screenshots

While the load test runs, open the AWS Console tabs and capture these screenshots in order:

1. **`01_alb_live_url.png`**: Browser showing the live ALB response `{"status": "Stream available", "instance": "i-..."}`.
2. **`02_tg_healthy_initial.png`**: EC2 $\rightarrow$ Target Groups $\rightarrow$ `hotstar-tg` $\rightarrow$ Targets showing initial 1 healthy target.
3. **`03_asg_config.png`**: EC2 $\rightarrow$ Auto Scaling Groups $\rightarrow$ `hotstar-asg` $\rightarrow$ Details showing Min 1, Desired 1, Max 4.
4. **`04_cloudwatch_50pct_alarm.png`**: CloudWatch $\rightarrow$ Alarms $\rightarrow$ `hotstar-cpu-high-scale-out` showing CPU line crossing the red 50% line and status changing to **In alarm**.
5. **`05_asg_scale_out_activity.png`**: EC2 $\rightarrow$ Auto Scaling Groups $\rightarrow$ `hotstar-asg` $\rightarrow$ Activity tab showing:
   *"Launching a new EC2 instance: i-XXXXX ... Cause: monitor alarm hotstar-cpu-high-scale-out"*.
6. **`06_tg_multiple_healthy_targets.png`**: EC2 $\rightarrow$ Target Groups $\rightarrow$ `hotstar-tg` $\rightarrow$ Targets showing multiple instances in **Healthy** state.
7. **`07_locust_terminal_summary.png`**: Terminal showing Locust completion summary table.
8. **`08_asg_scale_in_activity.png`**: Activity tab showing scale-in termination after the 15-minute cool-down.

Save all images to `results/screenshots/`.

---

## 7. Step 6: Generate the Required Figures (Python Analysis)

Once Locust finishes, stop the poller in Terminal 1 (Ctrl+C).

Run our analysis script [`analysis/plot.py`](file:///home/drixo/Projects/hotstar-cloud-scaling/analysis/plot.py):
```bash
python analysis/plot.py \
  --locust results/raw/locust_stats_history.csv \
  --instances results/raw/instances.csv \
  --out results/figures
```

### Outputs Generated:
* **`results/figures/F2_response_time_vs_instance_count.png`**:  
  **The primary mandatory course rubric deliverable** showing how response time drops as the ASG scales from 1 to multiple instances.
* **`results/figures/response_vs_instances.png`**:  
  Dual-axis graph plotting p95 latency and instance count across test time.
* Terminal printout with your exact p50, p95, and max instance metrics ready to copy into your final report table.

---

## 8. Step 7: 1-Click Clean Teardown (Zero Billing Guarantee)

Once all screenshots and data are captured:
1. Open the **CloudFormation** console.
2. Select the stack **`hotstar-scaling-poc`**.
3. Click the orange **Delete** button $\rightarrow$ confirm **Delete stack**.
4. CloudFormation will cleanly destroy all resources (ALB, ASG, EC2 instances, security groups, subnets, VPC) in ~2 minutes.
5. In the EC2 console, confirm that **Running Instances** is 0.

Your AWS bill will show **$0.00**.

---

## 9. Viva Defense: Manual Architecture Breakdown

Use this quick guide to answer viva questions about the architecture:

* **Why an Application Load Balancer (ALB) instead of a Network Load Balancer (NLB)?**  
  ALB operates at Layer 7 (HTTP/HTTPS), allowing path-based health checking (`/health`), connection multiplexing, and automatic traffic distribution across dynamic EC2 targets.
* **Why does the Auto Scaling Group use 50% CPU as the threshold?**  
  Spikes in live streaming happen within 60–90 seconds. Booting an EC2 instance, installing packages, and passing health checks takes 2–4 minutes (*scale-out lag*). Setting the threshold at 50% provides safety headroom so that existing instances do not crash from memory/CPU exhaustion while new capacity is booting.
* **What is the Health Check Grace Period (120s)?**  
  It gives a newly launched EC2 instance 2 minutes to boot, start Uvicorn, and initialize before the ASG evaluates its health. Without it, the ASG might prematurely terminate instances that are still starting up.
* **How does this PoC relate to Hotstar's actual architecture?**  
  This PoC proves the fundamental cloud mechanism of reactive autoscaling under CPU load. Hotstar observed that for predictable cricket matches, reactive autoscaling alone is too slow; hence, they combined reactive autoscaling with **concurrency ladders (pre-scaling)** and CDN shielding.
