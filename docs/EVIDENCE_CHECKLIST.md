# IT457 Hotstar Cloud Scaling — Final Deliverables & Evidence Checklist

**Course:** IT457 — Cloud Computing  
**Group:** 19 (Jill Chhagnani, Dhyey Patel, Jay Patel)  
**Theme 1:** Scalability & High-Traffic Events (Hotstar PoC)

---

## 1. Required Course Deliverables (Rubric)

| # | Deliverable | Description | Evidence Location | Status |
|:---|:---|:---|:---|:---:|
| **D1** | **Live Load Balancer URL** | Public ALB URL responding with JSON: `{"status": "Stream available", ...}` | Recorded in report & live during evaluation | [ ] |
| **D2** | **ASG Scaling Proof** | Screenshots of ASG dashboard showing instances spinning up automatically under load | `results/screenshots/01_asg_scale_out.png` | [ ] |
| **D3** | **Load Testing Report & Plots** | Graph plotting **Response Time vs. Instance Count** + Locust logs/HTML report | `results/figures/F2_response_time_vs_instance_count.png` | [ ] |

---

## 2. Screenshot Evidence Checklist (Capture During AWS Run)

Capture these 8 screenshots in order during your experiment:

- [ ] **Screenshot 1: Live ALB URL in Browser**  
  *URL:* `http://hotstar-alb-XXXXX.ap-south-1.elb.amazonaws.com/`  
  *Shows:* JSON response `{"status": "Stream available", "service": "hotstar-cloud-scaling-poc", "instance": "i-..."}`.  
  *Save as:* `results/screenshots/01_alb_live_url.png`

- [ ] **Screenshot 2: Target Group Healthy Target**  
  *AWS Console:* EC2 $\rightarrow$ Target Groups $\rightarrow$ `hotstar-tg` $\rightarrow$ **Targets** tab.  
  *Shows:* Target port 8000 with Health status `Healthy` (green checkmark).  
  *Save as:* `results/screenshots/02_tg_healthy_initial.png`

- [ ] **Screenshot 3: Auto Scaling Group Configuration**  
  *AWS Console:* EC2 $\rightarrow$ Auto Scaling Groups $\rightarrow$ `hotstar-asg` $\rightarrow$ **Details** tab.  
  *Shows:* Min: 1, Desired: 1, Max: 4.  
  *Save as:* `results/screenshots/03_asg_config.png`

- [ ] **Screenshot 4: CloudWatch 50% CPU Alarm Breach**  
  *AWS Console:* CloudWatch $\rightarrow$ Alarms $\rightarrow$ `hotstar-cpu-high-scale-out`.  
  *Shows:* Average CPU exceeding 50% threshold with red state indicator (`In alarm`).  
  *Save as:* `results/screenshots/04_cloudwatch_50pct_alarm.png`

- [ ] **Screenshot 5: ASG Activity Scale-Out Event**  
  *AWS Console:* EC2 $\rightarrow$ Auto Scaling Groups $\rightarrow$ `hotstar-asg` $\rightarrow$ **Activity** tab.  
  *Shows:* "Launching a new EC2 instance: i-XXXXX ... Cause: monitor alarm hotstar-cpu-high-scale-out".  
  *Save as:* `results/screenshots/05_asg_scale_out_activity.png`

- [ ] **Screenshot 6: Multiple Healthy Targets in Target Group**  
  *AWS Console:* EC2 $\rightarrow$ Target Groups $\rightarrow$ `hotstar-tg` $\rightarrow$ **Targets** tab.  
  *Shows:* 2 or more instances in `Healthy` state sharing traffic.  
  *Save as:* `results/screenshots/06_tg_multiple_healthy_targets.png`

- [ ] **Screenshot 7: Locust Load Test Terminal Summary**  
  *Shows:* Terminal summary output of Locust showing total requests, failures (0%), and latency percentiles.  
  *Save as:* `results/screenshots/07_locust_terminal_summary.png`

- [ ] **Screenshot 8: ASG Scale-In Event (Post-Test)**  
  *AWS Console:* EC2 $\rightarrow$ Auto Scaling Groups $\rightarrow$ `hotstar-asg` $\rightarrow$ **Activity** tab (after 15-20 min cool-down).  
  *Shows:* "Terminating EC2 instance ... Cause: monitor alarm hotstar-cpu-low-scale-in".  
  *Save as:* `results/screenshots/08_asg_scale_in_activity.png`

---

## 3. Results Summary Table Template (To Fill for Report)

| Metric | Baseline (Single Instance) | Autoscaled (1 to 4 Instances) |
|:---|:---:|:---:|
| **Peak Simulated Users** | 150 | 150 |
| **p50 Latency (ms)** | *(from Locust)* | *(from Locust)* |
| **p95 Latency (ms)** | *(from Locust)* | *(from Locust)* |
| **p99 Latency (ms)** | *(from Locust)* | *(from Locust)* |
| **Error Rate (%)** | *(from Locust)* | 0.0% |
| **Scale-Out Lag (seconds)** | N/A | *(time from spike start to 2nd instance healthy)* |
| **Max In-Service Instances** | 1 | *(usually 2 to 3)* |
| **Estimated AWS Cost** | $0.00 (Free Tier) | $0.00 (Free Tier) |

---

## 4. Key Viva Questions & Answers

1. **Q: Why did we set the CPU threshold to 50% instead of 80% or 90%?**  
   *A:* Booting a new EC2 instance, running user data, and passing ALB health checks takes 2 to 4 minutes (*scale-out lag*). If we wait until 80–90% CPU, sudden traffic spikes (like a cricket wicket or boundary) will cause request queues to overflow and clients to fail before new capacity becomes healthy. 50% gives the cluster a headroom safety buffer.

2. **Q: Why does Hotstar use pre-scaling ("ladders") rather than purely reactive autoscaling?**  
   *A:* In cricket live-streaming, 5–10 million viewers can arrive within 60–90 seconds. Because cloud instance provisioning takes minutes, reactive scaling always lags behind rapid traffic surges. Hotstar therefore pre-scales capacity in advance based on predicted viewership curves.

3. **Q: What is the purpose of the health check grace period?**  
   *A:* The health check grace period (120s) prevents the Auto Scaling Group from prematurely marking a newly launched instance as unhealthy and terminating it while Python packages and the application are still booting up.
