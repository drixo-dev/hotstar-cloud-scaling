# IT457 Hotstar Cloud Scaling — Final Deliverables & Evidence Checklist

**Course:** IT457 — Cloud Computing  
**Group:** 19 (Jill Chhagnani – 202301273, Dhyey Patel – 202301415, Jay Patel – 202301430)  
**Theme 1:** Scalability & High-Traffic Events (Hotstar PoC)

---

## 1. Required Course Deliverables (Rubric)

| # | Deliverable | Description | Evidence Location | Status |
|:---|:---|:---|:---|:---:|
| **D1** | **Live Load Balancer URL** | Public ALB URL responding with JSON: `{"status": "Stream available", ...}` | `http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com/` | **[x] Completed** |
| **D2** | **ASG Scaling Proof** | Screenshots of ASG dashboard showing instances spinning up automatically under load | `results/screenshots/05_cloudwatch_50pct_alarm.png`, `06_EC2_inst_scale.png`, `07_EC2_tg.png` | **[x] Completed** |
| **D3** | **Load Testing Report & Plots** | Graph plotting **Response Time vs. Instance Count** + Locust logs/HTML report | `results/figures/F2_response_time_vs_instance_count.png`, `results/report.html` | **[x] Completed** |

---

## 2. Screenshot Evidence Log (Captured on AWS ap-south-1)

All screenshots are stored in [`results/screenshots/`](file:///home/drixo/Projects/hotstar-cloud-scaling/results/screenshots/):

- [x] **Screenshot 1: Live ALB URL in Browser**  
  *File:* `results/screenshots/01_alb_live_url.png`  
  *Observation:* Browser displaying live HTTP 200 JSON response:  
  `{"status": "Stream available", "service": "hotstar-cloud-scaling-poc", "instance": "i-0af3ff28238614c6f"}`.

- [x] **Screenshot 2: Initial Healthy Target in Target Group**  
  *File:* `results/screenshots/02_hostar_tg_healthyInst.png`  
  *Observation:* Target group `hotstar-tg` on port 8000 with 1 healthy instance (`i-0af3ff28238614c6f`).

- [x] **Screenshot 3 & 4: Auto Scaling Group Initial Configuration**  
  *Files:* `results/screenshots/03_ASG_a.png`, `results/screenshots/04_ASG_b.png`  
  *Observation:* ASG `hotstar-asg` configured with Min: 1, Desired: 1, Max: 4, detailed 1-minute monitoring, and 120s grace period.

- [x] **Screenshot 5: CloudWatch 50% CPU Alarm Breach**  
  *File:* `results/screenshots/05_cloudwatch_50pct_alarm.png`  
  *Observation:* 1-hour view of `hotstar-cpu-high-scale-out` showing CPU utilization crossing the red 50% line, spiking to 59.25%, and entering `In alarm` state.

- [x] **Screenshot 6: ASG Scale-Out Activity History**  
  *File:* `results/screenshots/06_EC2_inst_scale.png`  
  *Observation:* Activity tab showing automatic launching of additional EC2 instances caused by `hotstar-cpu-high-scale-out`.

- [x] **Screenshot 7: Multiple Healthy Targets in Target Group**  
  *File:* `results/screenshots/07_EC2_tg.png`  
  *Observation:* Target group showing all scaled instances (`i-07fa1e9...`, `i-00a2e5...`, `i-0dbc6a...`, `i-0af3ff...`) healthy and sharing load.

- [x] **Screenshot 8 & 9: Locust Load Test Completion Summary**  
  *Files:* `results/screenshots/08_locust.png`, `results/screenshots/09_locust2.png`  
  *Observation:* Locust terminal showing 55,910 total requests, 99.58% success rate, response time percentiles, and request distribution.

- [x] **Screenshot 10 & 11: Scale-In & Connection Draining Proof**  
  *Files:* `results/screenshots/10_draining.png`, `results/screenshots/11_draining_asg.png`  
  *Observation:* Target group showing `Draining` state and ASG Activity showing termination of instances caused by `hotstar-cpu-low-scale-in` when traffic subsided.

---

## 3. Real Experiment Results Summary (55,910 Live Requests)

| Metric | Measured Value | Architectural Significance |
|:---|:---:|:---|
| **Total Test Duration** | 779 seconds (~13 minutes) | Matches Hotstar cricket match spike profile |
| **Total Requests Sent** | **55,910** | High-throughput stress test on ALB origin |
| **Overall Failure Rate** | **0.42%** (99.58% Success) | Transient timeouts occurred only during the 2-minute instance boot lag |
| **Median p50 Latency (1 Instance)** | 590.0 ms | Baseline performance before spike |
| **Median p95 Latency (1 Instance)** | 1,200.0 ms | Baseline 95th percentile |
| **Median p95 Latency (2 Instances)** | 2,100.0 ms | **Scale-Out Lag:** Peak traffic hit while new VMs were booting |
| **Median p95 Latency (3 Instances)** | 1,400.0 ms | Capacity relieved incoming request queue |
| **Median p95 Latency (4 Instances)** | **330.0 ms** | **84% reduction in p95 latency** once 4 instances were healthy |
| **Median p50 Latency (4 Instances)** | **73.0 ms** | Fast, responsive streaming delivery |
| **Max In-Service Instances** | **4** | Full scale-out capacity utilized |
| **Post-Test Scale-In** | 4 $\rightarrow$ 1 | Successfully drained connections and terminated extra VMs |
| **Total AWS Cost** | **$0.00** | 100% covered within AWS Free Tier |

---

## 4. Key Viva Questions & Answers

1. **Q: Why did we set the CPU threshold to 50% instead of 80% or 90%?**  
   *A:* Booting a new EC2 instance, running user data, and passing ALB health checks takes 2 to 4 minutes (*scale-out lag*). If we wait until 80–90% CPU, sudden traffic spikes (like a cricket wicket or boundary) will cause request queues to overflow and clients to fail before new capacity becomes healthy. 50% gives the cluster a headroom safety buffer.

2. **Q: Why did p95 latency temporarily rise to 2,100 ms when scaling to 2 instances, but drop to 330 ms at 4 instances?**  
   *A:* This directly demonstrates **Scale-Out Lag**. When the 150-user traffic surge hit, the initial instance was saturated before instance #2 became in-service and healthy in the target group. Once instances #3 and #4 joined the pool, request concurrency was evenly distributed, slashing latency by 84%.

3. **Q: Why does Hotstar use pre-scaling ("concurrency ladders") rather than purely reactive autoscaling?**  
   *A:* In live cricket streaming, 5–10 million viewers can arrive within 60–90 seconds. Because cloud VM provisioning takes minutes, reactive scaling always lags behind rapid traffic surges. Hotstar therefore pre-scales capacity in advance based on predicted viewership curves.

4. **Q: What is the purpose of the health check grace period (120s)?**  
   *A:* The health check grace period prevents the Auto Scaling Group from prematurely marking a newly launched instance as unhealthy and terminating it while Python packages and Uvicorn are still booting up.
