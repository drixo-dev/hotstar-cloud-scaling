# Cloud Scaling for Live Cricket Streaming
## Hotstar Case Study and Auto-Scaling Proof of Concept
**Course:** IT457 — Cloud Computing  
**Deliverable:** Week 2 Detailed Report (Case Analysis, Architecture & PoC Plan)  
**Group:** 19  
- **Dhyey Patel (202301415)** — Lead Cloud Systems Architect & Infrastructure Engineer (Primary Lead)  
- **Jill Chhagnani (202301273)** — Systems Research & Case Study Lead (2nd Priority)  
- **Jay Patel (202301430)** — Performance Analysis & Cost Modeling Associate (3rd Priority)  

**Date:** Revised November 2026  

---

## Executive Summary

Disney+ Hotstar (now JioHotstar) operates under an extreme infrastructure constraint: live cricket streaming traffic does not grow along smooth, predictable curves, but hits the backend as an abrupt, massive **"tsunami"**. Viewers join in millions within seconds of the match start, boundary hits, or unexpected wickets. Over eight years of platform growth, Hotstar's peak concurrent viewership surged more than thirteen-fold—from 4.7 million in 2017 to a company-reported **61.2 million concurrent viewers** during the 2025 ICC Champions Trophy final.

Engineering post-mortems published by Hotstar reveal that traditional reactive autoscaling—relying on threshold alarms to detect high load and launch virtual machines—consistently failed during sudden traffic spikes. Virtual machine provisioning, operating system boot, container extraction, and load balancer health checks create an unavoidable **scale-out lag** of 2 to 4 minutes. In cricket, several million viewers arrive in under 90 seconds, causing request queues to overflow, latencies to spike into multi-second timeouts, and client retries to initiate cascading backend collapse before reactive capacity can come online.

Hotstar resolved this bottleneck through a multi-tier defense:
1. **Pre-scaling with Concurrency Ladders (2018):** Capacity was manually or programmatically scheduled ahead of matches based on historic viewership models.
2. **Containerization & Custom Kubernetes Autoscalers (2019):** Moving from EC2 VMs to containers cut boot times and reduced compute waste tenfold.
3. **Multi-Cluster Infrastructure & Edge Protection (2023–2025):** Slicing workloads across 6 managed EKS clusters, adopting Envoy API gateways, and shielding origins with CDNs (Akamai/CloudFront) with 95%+ cache offload.

To evaluate the fundamental physics of cloud elasticity, Group 19 designs a small, rigorous **Cloud Proof of Concept (PoC)** on AWS following Theme 1 of the IT457 syllabus. The PoC implements a stateless **Python FastAPI** service deployed on EC2 `t3.micro` instances behind an **Application Load Balancer (ALB)** and managed by an **Auto Scaling Group (ASG)**. The group enforces an explicit CloudWatch alarm: **if average CPU utilization exceeds 50%, add another instance**. The system is evaluated under a match-shaped spike load using **Locust** to quantify latency, error rates, scale-out lag, and the performance relationship between response time and instance count.

---

## 1. Objectives, Scope, and Research Question

### 1.1 Objectives
1. **Case Study Analysis:** Synthesize primary engineering disclosures from Hotstar and AWS to document the evolution of traffic profiles, architectural bottlenecks, and cost levers.
2. **Cloud Infrastructure Implementation:** Provision a secure, automated 2-Availability-Zone cloud infrastructure on AWS using Infrastructure-as-Code (CloudFormation).
3. **Elasticity Verification:** Demonstrate that compute load exceeding 50% CPU automatically triggers dynamic scale-out (+1 instance) and traffic drops trigger scale-in.
4. **Empirical Measurement:** Quantify response time percentiles (p50, p95, p99), error rates, scale-out lag, and instance counts under an event-driven spike profile using Locust.

### 1.2 Research Question
> *Under a simulated live-event traffic spike, how do p95 response time, system throughput, and scale-out lag behave when a single-instance baseline is backed by an Application Load Balancer and an Auto Scaling Group enforcing a 50% CPU threshold?*

### 1.3 Scope Boundary
* **In Scope:** Stateless Python FastAPI service (`/`, `/health`, `/work`), AWS 2-AZ VPC networking, Application Load Balancers, Target Groups, EC2 Auto Scaling Groups, CloudWatch alarms, Locust load generation, and Python performance analysis.
* **Out of Scope:** Video encoding/transcoding pipelines, DRM licensing, edge CDN provider contracts, multi-region database replication, and any claim of matching Hotstar's 61.2M production concurrency on a student lab budget.

---

## 2. Case Background & Traffic Profile

### 2.1 Viewership Growth Evolution
Hotstar’s live cricket streaming records represent some of the highest concurrent digital broadcast events in internet history. All metrics below represent company-reported peak concurrency:

| Tournament Event | Date | Peak Concurrent Viewers | Architectural Era | Primary Source |
|:---|:---:|:---:|:---|:---:|
| **IPL 2018 Final** | May 2018 | 10.3 Million | EC2 Static Ladders | Hotstar Blog (Apr 2018) |
| **IPL 2019 Final** | May 2019 | 18.6 Million | Early Kubernetes Adoption | Hotstar Blog (Oct 2019) |
| **ICC World Cup Semi-Final** | Jul 2019 | 25.3 Million | Self-Managed Kubernetes | AWS re:Invent CMY302 (2019) |
| **ICC World Cup 2023 Final** | Nov 2023 | 59.0 Million | Managed Multi-Cluster EKS | Deccan Herald / JioStar Release |
| **IPL 2025 Final** | May 2025 | 55.0 Million | Managed EKS + Envoy | afaqs! Industry Report |
| **ICC Champions Trophy Final** | Mar 2025 | **61.2 Million** | 6 EKS Clusters + CDN Edge | JioStar Company Disclosure |

### 2.2 The "Tsunami" Traffic Dynamic
Unlike e-commerce (e.g., Amazon Prime Day) where traffic ramps up over hours, live cricket demand is hyper-concentrated:
* **The Match Start Shock:** 6 to 8 million viewers launch the application within 120 seconds of the first ball. Watch-page API traffic jumps 400% to 500% in this two-minute window.
* **Wicket & Boundary Spikes:** A star player entering the pitch or a crucial wicket causes instant notification-driven traffic surges of 300% within 30 seconds.
* **Post-Match Drop:** When the final ball is bowled, 70% of viewers exit the stream within 60 seconds, flooding homepage APIs with navigation requests before dropping to near-zero.
* **Scale-Out Lag Mathematics:** In 2019, viewership grew at over **1,000,000 users per minute**. Standard EC2 instance launch, initialization, and health checks took roughly 2.5 minutes. Consequently, **2.5 million users arrive before a single additional server can become healthy**, proving why reactive scaling alone causes outages during cricket.

---

## 3. Architecture Across Three Eras

```
ERA 1 (2018): EC2 + Concurrency Ladders
[Viewers] ──> [CloudFront/Akamai] ──> [200+ Classic Load Balancers] ──> [Static EC2 Pools]
(Problem: Reactive scaling too slow; pre-scaling resulted in massive idle cost)

ERA 2 (2019): Self-Managed Kubernetes & Custom Autoscaler
[Viewers] ──> [CDN Edge] ──> [ALBs] ──> [2 Large K8s Clusters] ──> [Custom Autoscaler Pods]
(Outcome: 10x compute reduction; Problem: K8s master node bottlenecks & IP exhaustion)

ERA 3 (2023–2025): Multi-Cluster EKS & Envoy Gateway
[Viewers] ──> [CDN Shield (95% cache)] ──> [Envoy Gateway] ──> [6 EKS Clusters as 1 DC]
(Outcome: 61.2M peak concurrency; fine-grained subnetting and graceful degradation)
```

### Era 1 (2018): Monolithic EC2 and Static "Ladders"
* Infrastructure: Monolithic services running directly on EC2 instances behind over 200 Classic Load Balancers.
* Scaling Strategy: Reactive autoscaling was disabled because it lagged behind traffic spikes. Instead, engineers used **concurrency ladders**: estimating viewer count 30 minutes in advance and pre-provisioning hundreds of idle EC2 instances.
* Limitations: Enormous cloud compute waste during slow matches; lack of flexibility if a match unexpectedly became thrilling; AWS API rate-limiting during bulk EC2 provisioning.

### Era 2 (2019): Self-Managed Kubernetes & Shadow Autoscaling
* Infrastructure: Migration of core services to Docker containers running on two massive self-managed Kubernetes clusters on EC2.
* Scaling Strategy: Developed a proprietary custom autoscaler that evaluated traffic velocity rather than standard CPU alone. Ran the autoscaler in "shadow mode" for months before trusting it with production traffic.
* Outcomes: Delivered 2x peak concurrency (25.3M) with roughly **10x less compute cost** compared to Era 1 by packing containers tightly onto Spot instances.
* Bottlenecks: A single cluster with thousands of pods overwhelmed the Kubernetes API Server (etcd locking), and AWS VPC IP address pools ran out of allocatable IPs.

### Era 3 (2023–2025): Multi-Cluster Managed EKS & Envoy Mesh
* Infrastructure: Sliced workloads across **six Amazon EKS clusters** unified under an Envoy API Gateway, eliminating over 200 individual load balancers that previously required pre-warming tickets with AWS support.
* Bottlenecks Solved:
  * **IP Exhaustion:** Moved from `/24` subnets to large `/19` subnets across multiple AZs.
  * **NAT Gateway Bottleneck:** Shifted NAT Gateways from per-AZ to per-subnet to prevent cross-AZ bandwidth saturation.
  * **Controlled Degradation ("Jettison"):** During peak spikes, non-critical features (comments, social feeds, recommendation widgets) are programmatically shed so video delivery manifests receive 100% of origin compute.

---

## 4. Cloud Proof of Concept (PoC) Design

### 4.1 System Architecture
Following Theme 1 of the IT457 guide, our PoC isolates the **compute elasticity and scale-out lag mechanics** of the origin tier:

```
[Locust Load Generator (Laptop / External Client)]
                     │ (Spike: 20 -> 150 Users)
                     ▼
       [Application Load Balancer (Port 80)]
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
         [Auto Scaling Group (1 to 4)]
                     │
      [CloudWatch Alarm: CPU > 50%]
```

### 4.2 Application Design (`app.py`)
The application is implemented in **Python 3.12** using **FastAPI** and served by **Uvicorn**:
* `GET /`: Returns `{"status": "Stream available", "instance": INSTANCE_ID}`.
* `GET /health`: Returns HTTP 200 `{"ok": true, "status": "healthy"}` for ALB health checking every 15 seconds.
* `GET /work?n=300000`: Executes controlled arithmetic iterations, consuming ~30–50 ms of CPU per request. Under concurrent Locust streams, this drives multi-core CPU utilization above 50%, triggering the ASG alarm.

### 4.3 CloudFormation Infrastructure-as-Code (`hotstar-fastapi-cfn.yaml`)
* **VPC:** 2 Availability Zones (`10.50.0.0/16`) in `ap-south-1` (Mumbai) with public subnets and an Internet Gateway.
* **Security:** ALB accepts public HTTP 80; EC2 instances accept port 8000 exclusively from the ALB security group.
* **Launch Template:** Amazon Linux 2023 on Free Tier `t3.micro` (2 vCPUs, 1 GB RAM). Detailed CloudWatch monitoring enabled (1-minute metrics). EC2 UserData installs Python, writes `app.py`, and starts a systemd service with `workers=2`.
* **Auto Scaling Group:** Min: 1, Desired: 1, Max: 4. Target Group health check grace period: 120s.
* **Scaling Policies & Alarms:**
  * **Scale-Out:** CloudWatch Alarm triggers when average ASG CPU > 50% for two consecutive 60-second periods $\rightarrow$ Adds 1 instance (+1) with a 120s cooldown.
  * **Scale-In:** CloudWatch Alarm triggers when average ASG CPU < 20% for ten consecutive 60-second periods $\rightarrow$ Removes 1 instance (-1) with a 300s cooldown.

---

## 5. Experiment Plan & Load Profile

### 5.1 The Match-Shaped Load Profile
The load test is implemented in Python using **Locust** (`loadtest/locustfile.py`) to simulate an event-driven cricket surge:
1. **Stage 1 (0–120s):** 20 users (steady match buildup baseline).
2. **Stage 2 (120–180s):** Rapid ramp to 150 users (the match-start tsunami spike).
3. **Stage 3 (180–600s):** 150 sustained users (holds pressure to test ASG scale-out and observe scale-out lag).
4. **Stage 4 (600–720s):** Drop to 20 users (traffic subsides).
5. **Stage 5 (720–780s):** Tail baseline recovery (observing scale-in connection draining).

### 5.2 Planned Experiments Table
| Run ID | Configuration | Min / Desired / Max | Target Workload | Objective |
|:---|:---|:---:|:---:|:---|
| **E0** | Smoke Test | 1 / 1 / 1 | 5 concurrent users | Verify ALB health, `/health` 200 OK, and DNS resolution |
| **E1** | Baseline (Fixed) | 1 / 1 / 1 | 150 users spike | Measure latency degradation and saturation on a single instance |
| **E2** | Auto-Scaled (Elastic) | 1 / 1 / 4 | 150 users spike | Measure scale-out lag, CPU breach, instance addition, and latency recovery |
| **E3** | Scale-In Verification | 4 $\rightarrow$ 1 | Post-test idle | Verify ALB connection draining and graceful VM termination |

---

## 6. Measurements, Metrics, and Analysis Framework

| Metric | Measurement Tool | Target Observation |
|:---|:---|:---|
| **p50 / p95 / p99 Latency** | Locust CSV History | Quantify user response time degradation during spike and recovery after scale-out |
| **Error Rate (%)** | Locust Aggregated Summary | Measure HTTP 502/504 timeouts caused by request queuing during scale-out lag |
| **Scale-Out Lag (seconds)** | ASG Activity History vs Locust Start | Time elapsed between spike arrival and newly launched instance reaching **Healthy** status in Target Group |
| **In-Service Capacity** | Real-Time ASG Poller (`poller.py`) | Track instantaneous server count (1 $\rightarrow$ 2 $\rightarrow$ 3 $\rightarrow$ 4 instances) |
| **CPU Utilization (%)** | CloudWatch Metric Alarm | Verify breach of the 50% threshold and subsequent load distribution |
| **AWS Billing Cost** | AWS Budgets & Free Tier Tracker | Verify total expenditure remains strictly **$0.00** |

---

## 7. Team Contributions and Work Allocation

Work distribution is allocated based on technical complexity and individual ownership:

| Member | Role & Ownership | Primary Responsibilities | Evidence Owned |
|:---|:---|:---|:---|
| **Dhyey Patel** *(202301415)* | **Lead Cloud Systems Architect & Infrastructure Engineer** *(Primary Lead - ~60%)* | • Lead end-to-end cloud architecture design.<br>• Authored Python FastAPI microservice (`app.py`) and multi-worker Dockerfile.<br>• Developed AWS CloudFormation IaC (`hotstar-fastapi-cfn.yaml`) for 2-AZ VPC, ALB, and ASG.<br>• Implemented CloudWatch 50% CPU alarms and step-scaling policies.<br>• Conducted AWS live deployment in `ap-south-1` and smoke testing.<br>• Executed Locust load testing and developed ASG real-time instance poller (`poller.py`). | Live ALB DNS URL, CloudFormation template, AWS Console infrastructure, CloudWatch alarms, Locust execution, and raw metrics. |
| **Jill Chhagnani** *(202301273)* | **Systems Research & Case Study Lead** *(2nd Priority - ~25%)* | • Primary-source literature research across Hotstar engineering publications.<br>• Extracted architectural evolution across 3 eras (2018–2025) and concurrency figures (61.2M).<br>• Designed architectural flow diagrams comparing Hotstar production to the PoC origin tier.<br>• Authored problem statement, scale-out lag formulation, and case background sections. | Research claims log, system architecture diagrams, and case study report drafting. |
| **Jay Patel** *(202301430)* | **Performance Analysis & Cost Modeling Associate** *(3rd Priority - ~15%)* | • Analyzed load test telemetry logs, verifying latency percentiles and error metrics.<br>• Formulated AWS Free Tier zero-cost verification model ($0.00) vs. enterprise pricing estimates.<br>• Conducted data validation across test runs and performed cross-review for report submission and viva defense. | Results analysis tables, AWS pricing calculations, and viva review documentation. |

---

## 8. References

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
