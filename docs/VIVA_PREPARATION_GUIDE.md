# IT457 Viva Defense Preparation Guide
## Group 19: Hotstar Cloud Scaling Proof of Concept

This document is a private preparation guide for Group 19 members for the Week 5 Viva. It is separate from the academic reports submitted to course instructors.

---

### Core Viva Talking Points (5-Minute Walkthrough)

1. **Problem Statement:** Live cricket traffic arrives as an abrupt "tsunami" (e.g. 6–8 million viewers in 120 seconds). Standard reactive autoscaling fails because virtual machine provisioning takes 2–4 minutes (*scale-out lag*), causing request timeouts and cascading client retries before new servers boot.
2. **Hotstar's Architectural Solution:** 
   - 2018: Pre-warmed "concurrency ladders" on EC2.
   - 2019: Containerization on self-managed Kubernetes with custom shadow autoscalers.
   - 2023–2025: Datacenter abstraction over 6 managed EKS clusters with an internal Envoy gateway mesh (eliminating 200+ external ALBs and hairpinning), Karpenter sub-minute node scaling, and graceful degradation ("Jettison").
3. **Our AWS Proof of Concept:**
   - 2-AZ VPC in `ap-south-1` (Mumbai).
   - Public Application Load Balancer (`hotstar-alb`) on port 80.
   - Multi-AZ Target Group (`hotstar-tg`) with `/health` checks every 15s.
   - Auto Scaling Group (`hotstar-asg`) with min 1, max 4, desired 1.
   - CloudWatch Alarm: CPU >= 50% triggers scale-out (+1); CPU <= 20% triggers scale-in (-1).
   - FastAPI multi-worker microservice with `/work?n=300000` consuming ~30 ms CPU per request.
4. **Empirical Results:**
   - 13-minute match-shaped Locust load test, 55,910 total requests, 99.58% success.
   - Latency jumped to 2,100 ms during the scale-out lag window (instances booting).
   - Once all 4 instances were in service, p95 dropped to 330 ms (**84% tail latency reduction**), and median p50 latency dropped to 73 ms.
   - Verified connection draining (30s) during post-test scale-in down to 1 instance.
   - Total AWS expenditure: **$0.00** (Free Tier).

---

### Live Demo Cheat Sheet (Scaling Out & Scaling In)

When asked to demonstrate live autoscaling, run:
```bash
# Make sure the virtual environment is active (or prefix with .venv/bin/)
source .venv/bin/activate
locust -f loadtest/locustfile.py --headless -u 60 -r 10 --run-time 3m --host http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com
```

**Timeline of what to show on screen:**
1. **$t = 0\text{s} - 30\text{s}$ (Traffic Influx):** Locust spawns 60 users (10/s) hitting `/work?n=300000`. Show the Locust terminal displaying ~120 req/s.
2. **$t = 60\text{s}$ (Alarm Trigger):** In AWS Console $\rightarrow$ CloudWatch Alarms, show `hotstar-cpu-high-scale-out` transitioning from `OK` to `ALARM` as CPU crosses 50%.
3. **$t = 90\text{s} - 120\text{s}$ (Scale-Out):** In EC2 Console $\rightarrow$ Auto Scaling Groups $\rightarrow$ `hotstar-asg` $\rightarrow$ **Activity History**, show the event: `Launching a new EC2 instance`. Show Desired Capacity increasing to 2.
4. **$t = 120\text{s} - 150\text{s}$ (Target Registration & Latency Drop):** In Target Groups $\rightarrow$ `hotstar-tg`, show the new instance changing from `initial` to `healthy`. Point out in Locust that response latency drops significantly.
5. **$t = 180\text{s}$ (Test Ends):** The 3-minute timer stops Locust automatically. Show traffic drops to 0.
6. **$t = 300\text{s}$ (Scale-In & Connection Draining):** As CPU stays below 20%, CloudWatch alarm `hotstar-cpu-low-scale-in` triggers. Under Target Groups, show the instance in **`Draining`** status (30s delay) before terminating cleanly.

---

### Key Questions & Answers

#### Q1: Why did you pick 50% CPU as the scaling threshold instead of 80% or 90%?
**Answer:** Because of **scale-out lag**. When a traffic surge hits, booting an EC2 instance, running cloud-init UserData, initializing Uvicorn workers, and passing two consecutive 15-second ALB health checks takes approximately 2 to 3 minutes. If the threshold were set at 80% or 90%, the existing instance would saturate at 100% CPU, exhaust socket queues, and crash while waiting for new capacity. Setting the threshold at 50% provides safety headroom so existing instances continue serving traffic without dropping connections while new capacity boots.

#### Q2: What is "scale-out lag", and where does it appear in your data?
**Answer:** Scale-out lag is the delay between a metric breach (CPU > 50%) and the moment newly launched instances reach healthy in-service status behind the load balancer. In our data, it appears clearly at $t = 120\text{s}$ to $t = 240\text{s}$. When the 150-user spike hit, median p95 latency jumped to 2,100 ms and 234 requests timed out because the single baseline instance was saturated while instance #2 was still booting. Once instances #3 and #4 joined the pool, request concurrency was distributed and latency plummeted to 330 ms.

#### Q3: What is the "service hairpinning" problem in Hotstar's Era 2, and how did Envoy solve it?
**Answer:** In Era 2 (self-managed Kubernetes), internal microservices had dedicated external ALBs. When Service B needed to call Service A, it made an HTTP call to `service-a.hotstar.com`, which resolved via Route 53 to an external ALB outside the cluster. The traffic hairpinned out of the node, traversed AWS external networking, and re-entered the cluster via NodePort. This required 200+ ALBs to be manually pre-warmed with AWS support tickets before every tournament and exhausted the NodePort port range (30000–32767). In Era 3, Hotstar deployed an internal Envoy API Gateway mesh. Service calls now resolve directly within the private VPC network, eliminating 200+ ALBs, eliminating hairpinning, and eliminating the need for pre-warming tickets.

#### Q4: Why didn't you add a database (like MySQL or DynamoDB) to the PoC?
**Answer:** Two reasons:
1. **Rubric alignment:** Theme 1 evaluates *compute elasticity and autoscaling under traffic events*.
2. **Variable isolation:** In production streaming, origin video chunks (.m4s) and playlist manifests are static assets served from cache (95%+ CDN hit ratio). If millions of viewers hit a relational database on every request, the database connection pool would deadlock. Omitting a database isolates the Auto Scaling Group's CPU response from stateful I/O bottlenecks.

#### Q5: What is connection draining (deregistration delay)?
**Answer:** When an Auto Scaling Group terminates an instance during scale-in, connection draining tells the Application Load Balancer to stop sending new requests to that instance while allowing existing in-flight HTTP requests to complete within a configured grace period (30 seconds in our setup). This ensures zero dropped requests during scale-in.

#### Q6: Why did you use Python FastAPI instead of Node.js?
**Answer:** Python FastAPI offers high asynchronous performance with native Pydantic data validation and clean concurrency via Uvicorn. To saturate CPU across multi-core EC2 instances (`t3.micro` has 2 vCPUs), we configured Uvicorn with 2 worker processes and implemented an arithmetic compute endpoint (`/work?n=300000`).

#### Q7: How does your PoC relate to Hotstar's actual scale?
**Answer:** Our PoC demonstrates the **fundamental physical principle** of cloud elasticity, scale-out lag, and threshold headroom at small scale (150 users across 4 instances). It models the stateless origin ingress tier. It leaves out the multi-CDN edge caching tier, video transcoding pipelines, multi-region replication, and the 61.2 million concurrent user scale.
