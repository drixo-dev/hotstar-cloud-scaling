import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set up figure
fig, ax = plt.subplots(figsize=(14, 8.5), dpi=300)
ax.set_xlim(0, 14)
ax.set_ylim(0, 8.5)
ax.axis('off')

# Color palette
bg_color = "#F8FAFC"
fig.patch.set_facecolor(bg_color)

c_vpc_border = "#94A3B8"
c_vpc_fill = "#FFFFFF"
c_subnet_border = "#CBD5E1"
c_subnet_fill = "#F1F5F9"
c_alb = "#0284C7"       # Blue
c_ec2 = "#F97316"       # AWS Orange
c_cw = "#DC2626"        # CloudWatch Red
c_asg = "#10B981"       # ASG Emerald
c_client = "#4F46E5"    # Indigo
c_text_dark = "#0F172A"
c_text_muted = "#475569"

# Helper for rounded boxes
def draw_card(ax, x, y, w, h, bg, border, lw=1.5, title=None, subtitle=None, badge=None, badge_color="#334155"):
    box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12,rounding_size=0.15",
                                 facecolor=bg, edgecolor=border, linewidth=lw, zorder=2)
    ax.add_patch(box)
    if badge:
        bbox_props = dict(boxstyle="round,pad=0.2", facecolor=badge_color, edgecolor="none")
        ax.text(x + 0.15, y + h - 0.25, badge, fontsize=8, color="white", weight="bold",
                bbox=bbox_props, zorder=3, va="center")
    if title:
        ty = y + h - 0.35 if not badge else y + h - 0.55
        ax.text(x + w/2, ty, title, fontsize=10.5, color=c_text_dark, weight="bold",
                ha="center", va="center", zorder=3)
    if subtitle:
        sy = y + 0.35
        ax.text(x + w/2, sy, subtitle, fontsize=8, color=c_text_muted,
                ha="center", va="center", zorder=3)

# 1. Main Title Header
ax.text(7, 8.1, "IT457 Proof of Concept: Multi-AZ AWS Scalability Architecture",
        fontsize=16, weight="bold", color=c_text_dark, ha="center")
ax.text(7, 7.75, "Theme 1: Automated Horizontal Elasticity (Locust → ALB → Multi-AZ ASG with CloudWatch Metric Alarms)",
        fontsize=9.5, color=c_text_muted, ha="center")

# 2. Client / Load Generator Card (Locust)
draw_card(ax, 0.4, 3.8, 2.2, 2.6, "#EEF2FF", c_client, lw=2, badge="TRAFFIC SOURCE", badge_color=c_client)
ax.text(1.5, 5.3, "Locust Swarm\nLoad Engine", fontsize=11, weight="bold", color="#312E81", ha="center")
ax.text(1.5, 4.4, "• Up to 250 Users\n• Hatch: 20 users/s\n• /work & /health\n• CPU Burn Workload", fontsize=8, color="#4338CA", ha="center")

# 3. Outer AWS Cloud Boundary
aws_box = patches.FancyBboxPatch((3.0, 0.5), 10.6, 6.9, boxstyle="round,pad=0.2,rounding_size=0.25",
                                 facecolor="#FFFFFF", edgecolor="#CBD5E1", linewidth=1.5, linestyle="--", zorder=1)
ax.add_patch(aws_box)
ax.text(3.3, 7.15, "AWS Cloud Region: ap-south-1 (Mumbai)", fontsize=9.5, weight="bold", color="#475569")

# 4. VPC Boundary
vpc_box = patches.FancyBboxPatch((3.3, 0.8), 10.0, 6.1, boxstyle="round,pad=0.15,rounding_size=0.2",
                                facecolor="#F8FAFC", edgecolor=c_vpc_border, linewidth=1.5, zorder=1)
ax.add_patch(vpc_box)
ax.text(3.6, 6.65, "VPC: 10.0.0.0/16 (Dual Availability Zone Deployment)", fontsize=9, weight="bold", color="#334155")

# 5. Application Load Balancer
draw_card(ax, 3.8, 3.8, 2.3, 2.4, "#E0F2FE", c_alb, lw=2, badge="PUBLIC INGRESS", badge_color=c_alb)
ax.text(4.95, 5.25, "Application\nLoad Balancer", fontsize=11, weight="bold", color="#0369A1", ha="center")
ax.text(4.95, 4.4, "hotstar-alb-*\n• Port 80 (HTTP)\n• Cross-Zone Balancing\n• Health: /health (15s)", fontsize=7.5, color="#0284C7", ha="center")

# 6. Target Group & ASG Outer Box
asg_outer = patches.FancyBboxPatch((6.6, 1.1), 6.4, 4.3, boxstyle="round,pad=0.15,rounding_size=0.2",
                                   facecolor="#ECFDF5", edgecolor=c_asg, linewidth=1.8, linestyle=":", zorder=2)
ax.add_patch(asg_outer)
ax.text(6.8, 5.15, "Auto Scaling Group: hotstar-asg (Min: 1, Max: 4, Desired: 1)", fontsize=9.5, weight="bold", color="#065F46")

# Subnet A Box (ap-south-1a)
subA_box = patches.FancyBboxPatch((6.9, 1.4), 2.8, 3.4, boxstyle="round,pad=0.1,rounding_size=0.15",
                                  facecolor="#FFFFFF", edgecolor=c_subnet_border, linewidth=1.2, zorder=3)
ax.add_patch(subA_box)
ax.text(8.3, 4.5, "Public Subnet 1\n(ap-south-1a | 10.0.1.0/24)", fontsize=8, weight="bold", color="#475569", ha="center")

# EC2 Instance 1 (Base / Primary)
draw_card(ax, 7.1, 2.9, 2.4, 1.3, "#FFF7ED", c_ec2, lw=1.5, badge="EC2-AZ-A (Active)", badge_color=c_ec2)
ax.text(8.3, 3.4, "t3.micro (FastAPI)", fontsize=9, weight="bold", color="#C2410C", ha="center")
ax.text(8.3, 3.1, "Uvicorn (Multi-worker)", fontsize=7.5, color="#9A3412", ha="center")

# EC2 Instance 2 (Scale-out target)
draw_card(ax, 7.1, 1.6, 2.4, 1.15, "#FAFAFA", "#94A3B8", lw=1.2, badge="EC2-AZ-A (Scale-Out)", badge_color="#64748B")
ax.text(8.3, 2.05, "t3.micro (Dynamically Added)", fontsize=8, weight="bold", color="#475569", ha="center")

# Subnet B Box (ap-south-1b)
subB_box = patches.FancyBboxPatch((9.9, 1.4), 2.8, 3.4, boxstyle="round,pad=0.1,rounding_size=0.15",
                                  facecolor="#FFFFFF", edgecolor=c_subnet_border, linewidth=1.2, zorder=3)
ax.add_patch(subB_box)
ax.text(11.3, 4.5, "Public Subnet 2\n(ap-south-1b | 10.0.2.0/24)", fontsize=8, weight="bold", color="#475569", ha="center")

# EC2 Instance 3 (Scale-out AZ-B)
draw_card(ax, 10.1, 2.9, 2.4, 1.3, "#FAFAFA", "#94A3B8", lw=1.2, badge="EC2-AZ-B (Scale-Out)", badge_color="#64748B")
ax.text(11.3, 3.4, "t3.micro (FastAPI)", fontsize=9, weight="bold", color="#475569", ha="center")
ax.text(11.3, 3.1, "Capacity Expansion", fontsize=7.5, color="#64748B", ha="center")

# EC2 Instance 4 (Peak Spike AZ-B)
draw_card(ax, 10.1, 1.6, 2.4, 1.15, "#FAFAFA", "#94A3B8", lw=1.2, badge="EC2-AZ-B (Max Peak)", badge_color="#64748B")
ax.text(11.3, 2.05, "t3.micro (Dynamically Added)", fontsize=8, weight="bold", color="#475569", ha="center")

# 7. CloudWatch Control Plane (Top Right)
draw_card(ax, 7.8, 5.65, 4.9, 1.05, "#FEF2F2", c_cw, lw=1.8, badge="TELEMETRY & ALARMS", badge_color=c_cw)
ax.text(10.25, 6.2, "AWS CloudWatch Metrics & Scaling Policies", fontsize=9.5, weight="bold", color="#991B1B", ha="center")
ax.text(10.25, 5.85, "Scale-Out: CPU >= 50% (1x60s) → Add 1-2 Instances | Scale-In: CPU <= 20% (3x60s) → Drop to 1",
        fontsize=7.2, color="#B91C1C", ha="center")

# Connection Arrows
# Client -> ALB
ax.annotate("", xy=(3.8, 5.0), xytext=(2.6, 5.0),
            arrowprops=dict(arrowstyle="-|>", color=c_client, lw=2.5, mutation_scale=15))
ax.text(3.2, 5.2, "HTTP / 250 U", fontsize=7.5, weight="bold", color=c_client, ha="center")

# ALB -> Subnet A
ax.annotate("", xy=(6.9, 4.0), xytext=(6.1, 4.8),
            arrowprops=dict(arrowstyle="-|>", color=c_alb, lw=2, mutation_scale=12))
# ALB -> Subnet B
ax.annotate("", xy=(9.9, 4.0), xytext=(6.1, 4.6),
            arrowprops=dict(arrowstyle="-|>", color=c_alb, lw=2, mutation_scale=12))

# CloudWatch -> ASG trigger
ax.annotate("", xy=(10.25, 5.4), xytext=(10.25, 5.65),
            arrowprops=dict(arrowstyle="-|>", color=c_cw, lw=2, mutation_scale=12, linestyle="--"))

# Telemetry from Subnet to CloudWatch
ax.annotate("", xy=(7.8, 6.15), xytext=(7.5, 4.8),
            arrowprops=dict(arrowstyle="-|>", color="#94A3B8", lw=1.5, mutation_scale=10, linestyle="--"))
ax.text(7.2, 5.7, "CPU %", fontsize=7.5, weight="bold", color="#64748B", rotation=40)

plt.tight_layout()
plt.savefig("reports/figures/poc_aws_architecture.png", dpi=300, facecolor=bg_color, bbox_inches='tight')
print("Successfully generated reports/figures/poc_aws_architecture.png")
