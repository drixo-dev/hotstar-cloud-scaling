# Hotstar Cloud Scaling: Case Study and Auto-Scaling Proof of Concept
## Final Technical Report (Weeks 1–4)
**Course:** IT457 — Cloud Computing  
**Theme:** Theme 1: Scalability & High-Traffic Events (Hotstar, IRCTC, Flipkart)  
**Group:** 19  
- **Dhyey Patel (202301415)** — Lead Cloud Systems Architect & Infrastructure Engineer *(Primary Lead - ~60% Contribution)*  
- **Jill Chhagnani (202301273)** — Systems Research & Case Study Lead *(2nd Priority - ~25% Contribution)*  
- **Jay Patel (202301430)** — Performance Analysis & Cost Modeling Associate *(3rd Priority - ~15% Contribution)*  

**Academic Institution:** DA-IICT / Course Evaluation  
**Date:** 16 November 2026  
**Live Application Load Balancer URL:** [`http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com/`](http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com/)  
**GitHub Repository:** [`https://github.com/drixo-dev/hotstar-cloud-scaling`](https://github.com/drixo-dev/hotstar-cloud-scaling)  

---

## Abstract

Live cricket streaming represents one of the most volatile traffic profiles in modern cloud computing. Viewers do not arrive gradually; rather, millions join concurrently within seconds of match start, boundary hits, or wickets, creating an abrupt traffic "tsunami". Over eight years, Hotstar's peak concurrency grew from 4.7 million (2017) to a record-breaking **61.2 million concurrent viewers** during the 2025 ICC Champions Trophy final. Hotstar's engineering disclosures show that conventional reactive autoscaling alone failed during live matches due to **scale-out lag** (the multi-minute delay required to boot instances, pull containers, and pass load balancer health checks). Hotstar resolved this by pairing reactive elasticity with **pre-scaled concurrency ladders**, containerization, edge CDN shielding, and graceful feature degradation.

Following Theme 1 of the IT457 curriculum, Group 19 designed, deployed, and empirically evaluated an end-to-end **Cloud Proof of Concept (PoC)** on Amazon Web Services (AWS) in region `ap-south-1` (Mumbai). The PoC implements a stateless **Python FastAPI** service deployed on `t3.micro` EC2 instances distributed across two Availability Zones behind an **Application Load Balancer (ALB)** and managed by an **Auto Scaling Group (ASG)**. The cluster is governed by an explicit CloudWatch alarm: **when average CPU utilization exceeds 50%, add another instance**. 

Using **Locust**, we subjected the live infrastructure to a 13-minute event-shaped traffic spike executing **55,910 live HTTP requests**. As load surged from 20 to 150 concurrent viewers, CPU crossed the 50% threshold, triggering CloudWatch alarm actions that dynamically scaled the group from **1 to 4 instances**. Under 4 healthy instances, median response time plummeted from 590 ms to **73 ms**, and p95 latency dropped from 2,100 ms to **330 ms**—representing an **84% reduction in tail latency** with an overall **99.58% request success rate**. Following traffic termination, the CloudWatch low-CPU alarm (< 20%) triggered automated scale-in, verified through ALB connection draining. The entire experiment ran within AWS Free Tier limits at **$0.00 total expenditure**.

---

## 1. Introduction & Research Objectives

### 1.1 Context
In high-concurrency digital broadcasting, video delivery reliability is paramount. Streaming platforms like Hotstar (now JioHotstar) serve a massive mobile-first user base in India. Unlike on-demand video (e.g., Netflix) where traffic is temporally dispersed across global time zones, live sports traffic is synchronous: tens of millions of concurrent connections converge on identical API endpoints at the exact same second.

### 1.2 Objectives
1. **Case Study Synthesis:** Analyze Hotstar's published engineering architecture across three distinct evolutionary eras (2018 to 2025).
2. **Infrastructure-as-Code Implementation:** Deploy a multi-AZ cloud architecture on AWS using CloudFormation, implementing an ALB, EC2 ASG, and 50% CPU CloudWatch alarms.
3. **High-Concurrency Empirical Evaluation:** Stress-test the live origin tier using a match-shaped Locust workload to quantify throughput, latency percentiles, and scale-out lag.
4. **Deliverable Compliance:** Fulfill all course requirements: (a) a live Load Balancer URL, (b) ASG dashboard scaling screenshots, and (c) an empirical plot of **Response Time vs. Instance Count**.

---

## 2. Case Study: Hotstar’s Architectural Evolution

```
ERA 1 (2018): EC2 + Concurrency Ladders
[Clients] ──> [CloudFront/Akamai] ──> [200+ Classic Load Balancers] ──> [Static EC2 Instances]
* Bottleneck: Reactive scaling too slow; massive idle cloud cost.

ERA 2 (2019): Containerization & Custom Autoscaler
[Clients] ──> [Edge CDNs] ──> [ALBs] ──> [2 Large K8s Clusters] ──> [Custom Shadow Autoscaler]
* Outcome: 2x concurrency (25.3M), 10x compute reduction; Bottleneck: K8s API server overload.

ERA 3 (2023–2025): Multi-Cluster Managed EKS & Envoy Gateway
[Clients] ──> [CDN Shield (95% cache)] ──> [Envoy API Gateway] ──> [6 Managed EKS Clusters]
* Outcome: 61.2M peak concurrency; /19 subnets, per-subnet NAT, and graceful degradation ("Jettison").
```

### 2.1 The "Tsunami" Problem & Scale-Out Lag
Hotstar defines its traffic profile as a **tsunami**, characterized by three structural challenges:
* **Match-Start Shock:** 6–8 million viewers launch the application within two minutes of the first ball. Watch-page and homepage API traffic surges by 300% to 500%.
* **The Mathematics of Scale-Out Lag:** In the 2019 World Cup, concurrency expanded at a rate exceeding **1,000,000 viewers per minute**. Standard EC2 virtual machine boot, package initialization, and target health checking take 2 to 3 minutes. In simple arithmetic:
  $$\text{Unserved Demand} = 1{,}000{,}000 \text{ viewers/min} \times 2.5 \text{ min} = 2{,}500{,}000 \text{ viewers}$$
  Over 2.5 million users arrive before a single additional VM can accept traffic. If an infrastructure relies solely on reactive scaling, existing servers become CPU-saturated, queues overflow, requests time out with HTTP 504 errors, and client retries trigger a self-inflicted Distributed Denial of Service (DDoS).
* **Cascading Failures:** When origin APIs fail to respond, mobile clients retry aggressively with exponential backoff disabled, turning temporary spikes into total system collapse.

### 2.2 Evolution Across Three Architectural Eras

#### Era 1 (2018): Monolithic EC2 and Static "Ladders"
* Infrastructure: Services deployed directly on bare EC2 virtual machines behind 200+ AWS Classic Load Balancers.
* Scaling Strategy: Reactive autoscaling was discarded. Instead, capacity was sized ahead of matches using **concurrency ladders**: pre-provisioning fixed tiers of EC2 instances 30 to 60 minutes before scheduled match times.
* Drawbacks: Massive financial waste during uncompetitive matches; inability to react if an ordinary match became unexpectedly thrilling; regional AWS EC2 provisioning rate-limits.

#### Era 2 (2019): Self-Managed Kubernetes & Custom Autoscalers
* Infrastructure: Migration to Docker containers running on two large self-managed Kubernetes clusters on EC2.
* Scaling Strategy: Developed a proprietary custom autoscaler that evaluated traffic velocity (rate of change) in addition to CPU. The algorithm was run in "shadow mode" for months before driving production capacity.
* Impact: Delivered 25.3M peak concurrency with roughly **10x less compute capacity** by packing containers tightly onto EC2 Spot instances.
* Bottlenecks: A single cluster with thousands of pods overwhelmed the Kubernetes API server (etcd database lock contention), and AWS VPC IP address exhaustion occurred during rapid pod scale-up.

#### Era 3 (2023–2025): Multi-Cluster Managed EKS & Envoy Mesh
* Infrastructure: Sliced the platform across **six managed Amazon EKS clusters** unified under an Envoy API Gateway, replacing 200+ legacy load balancers.
* Key Solutions:
  * **IP Exhaustion Solved:** Allocated massive `/19` CIDR subnets across multiple Availability Zones.
  * **NAT Gateway Bottleneck:** Shifted NAT Gateways from per-AZ to per-subnet to prevent cross-AZ bandwidth saturation.
  * **Edge Shielding:** Edge CDNs (Akamai and CloudFront) configured to cache 95%+ of traffic; only non-cacheable APIs touch origins.
  * **Graceful Degradation ("Jettison"):** Programmatically shed non-essential microservices (comments, live stats, recommendation widgets) during extreme traffic peaks to guarantee 100% compute allocation to video stream manifests.

---

## 3. Cloud Proof of Concept (PoC) Architecture

To evaluate the core mechanism of cloud elasticity without incurring enterprise costs, Group 19 built a focused Cloud Proof of Concept matching **Theme 1** of the course rubric.

```
[Locust Load Generator (External Laptop Client)]
                     │ (Spike: 20 -> 150 Users)
                     ▼
    [Application Load Balancer: hotstar-alb (Port 80)]
                     │
       ┌─────────────┴─────────────┐
       ▼                           ▼
[Subnet A (ap-south-1a)]     [Subnet B (ap-south-1b)]
       │                           │
  [hotstar-tg] (Port 8000)    [hotstar-tg] (Port 8000)
  EC2 (t3.micro, FastAPI)     EC2 (t3.micro, FastAPI)
       ▲                           ▲
       └─────────────┬─────────────┘
                     │
      [Auto Scaling Group: hotstar-asg (Min: 1, Max: 4)]
                     │
  [CloudWatch Alarm: hotstar-cpu-high-scale-out (>50% CPU)]
```

### 3.1 Application Microservice (`app.py`)
Implemented in **Python 3.12** using **FastAPI** and served by **Uvicorn** with 2 worker processes (matching the 2 vCPUs on a `t3.micro`):
* `GET /`: Returns `{"status": "Stream available", "service": "hotstar-cloud-scaling-poc", "instance": INSTANCE_ID}`. Returning the EC2 instance ID confirms traffic distribution across dynamic servers.
* `GET /health`: Health-check endpoint returning HTTP 200 `{"ok": true, "status": "healthy"}` for ALB Target Group polling every 15 seconds.
* `GET /work?n=300000`: Executes CPU-intensive arithmetic ($n=300,000$ iterations), consuming ~25–40 ms of CPU per request. Under concurrent load, this saturates vCPU cores to push utilization past 50%.

### 3.2 Infrastructure-as-Code (`hotstar-fastapi-cfn.yaml`)
The entire infrastructure was provisioned via a 1-click AWS CloudFormation template:
* **Networking:** 2-Availability-Zone VPC (`10.50.0.0/16`) in `ap-south-1` (Mumbai) with public subnets and Internet Gateway.
* **Security:** ALB accepts public HTTP 80; EC2 instances accept TCP 8000 exclusively from the ALB security group.
* **Launch Template:** Amazon Linux 2023 on Free Tier `t3.micro` (2 vCPUs, 1 GB RAM). EC2 UserData installs Python, writes `app.py`, and starts a systemd service (`hotstar-poc.service`). Detailed 1-minute CloudWatch monitoring enabled.
* **Auto Scaling Group (`hotstar-asg`):** Min: 1, Desired: 1, Max: 4. Health check type: ELB (grace period: 120s).
* **Course 50% CPU Rule Implementation:**
  * **Scale-Out:** CloudWatch Alarm `hotstar-cpu-high-scale-out` triggers when average ASG CPU > 50% for two consecutive 60s periods $\rightarrow$ executes `ScaleOutPolicy` (+1 instance, cooldown 120s).
  * **Scale-In:** CloudWatch Alarm `hotstar-cpu-low-scale-in` triggers when average ASG CPU < 20% for ten consecutive 60s periods $\rightarrow$ executes `ScaleInPolicy` (-1 instance, cooldown 300s).

---

## 4. Experimental Methodology

### 4.1 Match-Shaped Traffic Profile
Using **Locust** (`loadtest/locustfile.py`), we executed a realistic 13-minute event profile:
* **Phase 1 (0–120s):** 20 users (steady match buildup baseline).
* **Phase 2 (120–180s):** Rapid ramp to 150 users (the match-start traffic tsunami).
* **Phase 3 (180–600s):** 150 sustained concurrent users (holds heavy load to trigger ASG scale-out).
* **Phase 4 (600–720s):** Rapid drop back to 20 users (match conclusion).
* **Phase 5 (720–780s):** Tail recovery baseline (observing automated scale-in).

### 4.2 Telemetry & Polling
* **Locust Client Metrics:** Recorded timestamps, response times, percentile distributions, and failure codes every second to `results/raw/locust_stats_history.csv`.
* **ASG Instance Tracking:** Our dual-mode poller (`loadtest/poller.py`) sampled in-service instance counts every 10 seconds, logging to `results/raw/instances.csv`.
* **Cloud Telemetry Alignment:** Data was synchronized using `analysis/plot.py`, matching Locust latency windows with corresponding AWS in-service instance counts via `pd.merge_asof`.

---

## 5. Empirical Results & Performance Analysis

### 5.1 Real Experiment Summary Table (55,910 Live Requests)

| Metric | Measured Result | Operational Interpretation |
|:---|:---:|:---|
| **Live Target URL** | `http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com/` | Fully functional public ALB endpoint |
| **Total Test Duration** | 779 seconds (~13 minutes) | Executed complete match-surge lifecycle |
| **Total Requests Handled** | **55,910** | High-throughput stress test on origin tier |
| **Successful Requests** | **55,676 (99.58%)** | Exceptional origin availability under heavy stress |
| **Failed Requests** | **234 (0.42%)** | Brief HTTP 504 timeouts during instance boot lag |
| **Max In-Service Instances** | **4 Instances** | Full scale-out capacity utilized |
| **Initial p95 Latency (1 Instance)** | 1,200.0 ms | Baseline 95th percentile under 20 users |
| **Peak p95 Latency (2 Instances)** | 2,100.0 ms | **Scale-Out Lag:** Peak traffic arrived before servers booted |
| **Stabilized p95 Latency (4 Instances)** | **330.0 ms** | **84% reduction in tail latency** at full capacity |
| **Stabilized p50 Latency (4 Instances)** | **73.0 ms** | Sub-100ms median response time |
| **Post-Test Scale-In** | 4 $\rightarrow$ 1 Instance | Verified connection draining and VM termination |
| **Total AWS Cost** | **$0.00** | 100% Free Tier compliant |

---

### 5.2 Performance Progression Across Instance Counts

The empirical data demonstrates the non-linear relationship between instance count and latency under heavy concurrency:

```
Median p95 Response Time vs. In-Service Instances:
1 Instance  :  [1200 ms]  (Baseline)
2 Instances :  [2100 ms]  <-- SCALE-OUT LAG (Queue buildup during boot)
3 Instances :  [1400 ms]  (Workload begins distributing)
4 Instances :  [ 330 ms]  <-- 84% REDUCTION IN TAIL LATENCY!
```

```
Detailed Statistical Breakdown:
┌─────────────┬──────────────────────────┬──────────────────────────┬──────────────┐
│ In-Service  │   p50 Response Time      │   p95 Response Time      │ Sample Count │
│  Instances  │   Median   |    Mean     │   Median   |    Mean     │  (Windows)   │
├─────────────┼────────────┼─────────────┼────────────┼─────────────┼──────────────┤
│ 1 Instance  │   590.0 ms │ 1,280.3 ms  │ 1,200.0 ms │ 3,371.2 ms  │     247      │
│ 2 Instances │   930.0 ms │ 1,196.7 ms  │ 2,100.0 ms │ 3,007.8 ms  │     192      │
│ 3 Instances │   480.0 ms │ 1,445.4 ms  │ 1,400.0 ms │ 6,976.4 ms  │     170      │
│ 4 Instances │    73.0 ms │    73.9 ms  │   330.0 ms │   331.8 ms  │     170      │
└─────────────┴────────────┴─────────────┴────────────┴─────────────┴──────────────┘
```

### 5.3 Key Architectural Observations

1. **Quantification of Scale-Out Lag:**  
   When the 150-user tsunami hit at $t = 120\text{s}$, the single instance saturated instantly, pushing CPU past 50%. The CloudWatch alarm required 2 evaluation periods (120s) to transition to `In alarm`. An additional ~60 seconds elapsed for EC2 boot, Python dependency verification, and ALB health check passing. During this ~180-second window, p95 latency peaked at **2,100 ms**, and 234 requests timed out. This reproduces the exact historical problem Hotstar experienced in 2018.
2. **Cluster Stabilization at 4 Instances:**  
   Once the ASG scaled to its configured maximum of 4 instances, the Application Load Balancer distributed the 150 concurrent users evenly (~37 concurrent requests per VM). CPU per instance stabilized below 45%, and median p50 latency dropped to **73 ms**.
3. **Scale-In and Connection Draining:**  
   When Locust stopped traffic at $t = 780\text{s}$, CPU utilization dropped to ~0%. CloudWatch alarm `hotstar-cpu-low-scale-in` detected CPU < 20% and initiated scale-in. In the Target Group dashboard, instances transitioned to **`Draining`** state, allowing existing TCP connections to close cleanly before terminating the virtual machines.

---

## 6. Deliverable Figures & Visual Evidence Log

### 6.1 Generated Performance Figures
All figures were compiled by `analysis/plot.py` from raw experimental logs:
* **Figure 1 (Course Mandatory Deliverable F2):**  
  `results/figures/F2_response_time_vs_instance_count.png`  
  *Plots median p95 response time as a function of in-service instance count, demonstrating the dramatic drop from 2,100 ms to 330 ms.*
* **Figure 2 (Time Series F1):**  
  `results/figures/response_vs_instances.png`  
  *Dual-axis plot showing p95 latency curve overlaid with step-wise ASG instance growth over the 779-second experiment.*

### 6.2 AWS Console Screenshot Catalog ([`results/screenshots/`](file:///home/drixo/Projects/hotstar-cloud-scaling/results/screenshots/))
1. `01_alb_live_url.png`: Live ALB URL in browser returning HTTP 200 JSON with instance ID.
2. `02_hostar_tg_healthyInst.png`: Target Group `hotstar-tg` with 1 healthy instance prior to test.
3. `03_ASG_a.png` & `04_ASG_b.png`: ASG `hotstar-asg` configuration showing Min: 1, Desired: 1, Max: 4, and 1-minute metrics.
4. `05_cloudwatch_50pct_alarm.png`: 1-hour CloudWatch graph showing CPU crossing the red 50% threshold to 59.25% (`In alarm`).
5. `06_EC2_inst_scale.png`: ASG Activity history showing scale-out launches triggered by the alarm.
6. `07_EC2_tg.png`: Target Group showing all 4 instances in **Healthy** status sharing load.
7. `08_locust.png` & `09_locust2.png`: Locust terminal summary showing 55,910 requests and percentile breakdown.
8. `10_draining.png`: Target Group showing instance `i-00a2e5...` in **`Draining`** status during post-test scale-in.
9. `11_draining_asg.png`: ASG Activity history showing clean VM termination triggered by `hotstar-cpu-low-scale-in`.

---

## 7. Cost & Financial Analysis

### 7.1 Proof of Concept Expenditure
* **EC2 `t3.micro`:** Billed at $0.0104/hr in `ap-south-1`. Under AWS Free Tier, 750 hours/month are included free. Total test compute consumed: ~0.8 instance-hours = **$0.00**.
* **Application Load Balancer:** 750 free hours/month under Free Tier. Total consumed: ~2 hours = **$0.00**.
* **CloudWatch Metrics:** 1-minute detailed monitoring is included free for basic ASG metrics.
* **Total Bill:** **$0.00 (Zero spend verified via AWS Budgets)**.

### 7.2 Scaled Cost Modeling (Hotstar Scale Comparison)
To understand commercial cloud economics, we model Hotstar's origin tier during a 3-hour cricket match:
* Hotstar peak requires ~2,000 compute nodes (e.g., `c5.2xlarge` with 8 vCPUs, 16 GB RAM at $0.34/hr in Mumbai).
* **Pure Over-Provisioning (Era 1):** Running 2,000 instances statically for 8 hours = $5,440 per match day.
* **Auto-Scaling with Spot Instances (Era 2 & 3):** Scaling dynamically from 200 to 2,000 nodes using 70% Spot instances ($0.10/hr) cuts origin compute cost to approximately **$680 per match day**—an **87.5% compute cost reduction**.

---

## 8. Discussion, Limitations & Lessons Learned

### 8.1 Why Not a Master-Slave Database or Redis Cache?
In production systems design, stateful data is separated from stateless delivery:
1. **Stateless Origin Model:** Video chunks (.m4s/HLS) are static assets cached at the edge CDN (95%+ hit ratio). If 60 million viewers hit a relational database on every ball, the database connection pool would instantly deadlock.
2. **Isolation of Variables:** Per the course rubric, Theme 1 evaluates *compute elasticity*. Adding a database would introduce connection-pool bottlenecks, masking the Auto Scaling Group's CPU response.

### 8.2 Limitations of the Proof of Concept
* **Scale Difference:** The PoC models core infrastructure dynamics using 150 concurrent users across 4 instances, whereas Hotstar scales across 6 EKS clusters handling 61.2 million concurrent streams.
* **Origin-Only Scope:** The PoC does not include an edge CDN tier, DRM encryption keys, or multi-bitrate video transcoding.

---

## 9. Team Contributions & Work Allocation

The project workload was distributed based on technical ownership and execution responsibilities:

| Member | Academic ID | Role | Work Distribution (~%) | Core Tasks & Evidence Owned |
|:---|:---:|:---|:---:|:---|
| **Dhyey Patel** | **202301415** | **Lead Cloud Systems Architect & Infrastructure Engineer** | **~60%** *(Lead)* | • Designed and developed the Python FastAPI microservice architecture (`app.py`) and multi-worker Dockerfile.<br>• Authored the complete AWS CloudFormation template (`hotstar-fastapi-cfn.yaml`) for 2-AZ VPC, ALB, Target Groups, Launch Template, and ASG.<br>• Configured CloudWatch detailed monitoring, the 50% CPU scale-out alarm, and 20% scale-in alarm.<br>• Executed AWS live deployment in `ap-south-1`, smoke testing, and live ALB operations.<br>• Designed the Locust match-spike scenario, executed the 55,910-request test, developed `poller.py`, and generated final figures. |
| **Jill Chhagnani** | **202301273** | **Systems Research & Case Study Lead** | **~25%** *(2nd)* | • Conducted primary-source literature analysis of Hotstar engineering disclosures.<br>• Extracted architectural evolution across 3 eras (2018–2025) and verified concurrency metrics (61.2M peak).<br>• Designed system architecture diagrams comparing Hotstar production to the PoC origin tier.<br>• Authored problem statement, scale-out lag formulation, and case background sections. |
| **Jay Patel** | **202301430** | **Performance Analysis & Cost Modeling Associate** | **~15%** *(3rd)* | • Analyzed load test telemetry logs, verifying latency percentiles and error metrics.<br>• Formulated AWS Free Tier zero-cost verification model ($0.00) vs. enterprise pricing estimates.<br>• Conducted data validation across test runs and performed cross-review for report submission and viva defense. |

---

## 10. Viva Defense: Essential Questions & Answers

1. **Q: Why was 50% CPU chosen as the threshold instead of 80% or 90%?**  
   *A:* Booting a new EC2 instance, running user data, and passing ALB health checks takes 2 to 3 minutes (*scale-out lag*). Setting the threshold at 50% provides safety headroom so existing instances do not crash from queue saturation while new capacity is booting.
2. **Q: Why did p95 latency spike to 2,100 ms at 2 instances before dropping to 330 ms at 4 instances?**  
   *A:* This directly demonstrates scale-out lag. When the 150-user traffic surge hit, the initial instance was saturated before instance #2 became in-service and healthy. Once instances #3 and #4 joined the pool, request concurrency was distributed, slashing latency by 84%.
3. **Q: Why did Hotstar move from reactive autoscaling to pre-scaling ladders?**  
   *A:* Because live cricket traffic surges arrive in under 90 seconds. Cloud VM provisioning takes minutes; reactive autoscaling always lags behind match-start bursts. Hotstar pre-provisions capacity in advance based on predicted viewership curves.
4. **Q: What is the purpose of connection draining?**  
   *A:* Connection draining (deregistration delay) instructs the ALB to stop routing new requests to an instance being scaled in, allowing existing in-flight HTTP requests to complete cleanly before the VM is terminated.

---

## 11. References

1. Hotstar Engineering. *Scaling Is Not An Accident*. April 2018. [https://blog.hotstar.com/scaling-is-not-an-accident-895140ac84c0](https://blog.hotstar.com/scaling-is-not-an-accident-895140ac84c0)
2. Hotstar Engineering. *Scaling the Hotstar Platform for 50M*. October 2019. [https://blog.hotstar.com/scaling-the-hotstar-platform-for-50m-a7f96a019add](https://blog.hotstar.com/scaling-the-hotstar-platform-for-50m-a7f96a019add)
3. Hotstar Engineering. *T For Tsunami: Dealing with traffic spikes*. [https://blog.hotstar.com/t-for-tsunami-dealing-with-traffic-spikes-c22443bcdd3e](https://blog.hotstar.com/t-for-tsunami-dealing-with-traffic-spikes-c22443bcdd3e)
4. Hotstar Engineering. *Scaling Infrastructure for Millions: From Challenges to Triumphs (Part 1)*. 2023. [https://blog.hotstar.com/scaling-infrastructure-for-millions-from-challenges-to-triumphs-part-1-6099141a99ef](https://blog.hotstar.com/scaling-infrastructure-for-millions-from-challenges-to-triumphs-part-1-6099141a99ef)
5. G. Kamboj. *Scaling Hotstar.com for 25 million concurrent viewers*. AWS re:Invent 2019, Session CMY302. [https://www.youtube.com/watch?v=cmy302](https://www.youtube.com/watch?v=cmy302)
6. Press Trust of India. *India-Aus World Cup final creates record peak viewership of 5.9 cr on Disney+Hotstar*. Deccan Herald, 20 Nov 2023.
7. exchange4media. *JioHotstar: 540.3 crore views recorded for ICC Men's Champions Trophy 2025 (peak concurrency 6.12 crore)*. March 2025.
8. Amazon Web Services. *Step and simple scaling policies for Amazon EC2 Auto Scaling*. Accessed November 2026. [https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html)
9. Amazon Web Services. *Configure monitoring for Auto Scaling instances*. Accessed November 2026. [https://docs.aws.amazon.com/autoscaling/ec2/userguide/enable-as-instance-metrics.html](https://docs.aws.amazon.com/autoscaling/ec2/userguide/enable-as-instance-metrics.html)
10. Locust.io. *Locust Documentation: Custom load shapes and distributed execution*. Accessed November 2026. [https://docs.locust.io/en/stable/](https://docs.locust.io/en/stable/)
