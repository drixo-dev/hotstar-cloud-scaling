#!/usr/bin/env python3
"""
build_all_svg_diagrams.py
Generates 100% custom, publication-quality, crisp vector SVG diagrams and renders
them to 2400px wide, 300 DPI PNGs via rsvg-convert.

Zero third-party branding. Zero overlapping text, clipped labels, or awkward lines.
All diagrams are designed from scratch for Group 19 (Hotstar Cloud Scaling PoC).
"""

import os
import subprocess

OUTPUT_DIR = "reports/figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def render_svg(svg_content: str, png_filename: str, width: int = 2400):
    svg_filename = png_filename.replace(".png", ".svg")
    svg_path = os.path.join(OUTPUT_DIR, svg_filename)
    png_path = os.path.join(OUTPUT_DIR, png_filename)

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content.strip())

    cmd = ["rsvg-convert", "-w", str(width), svg_path, "-o", png_path]
    subprocess.run(cmd, check=True)
    size_kb = os.path.getsize(png_path) / 1024
    print(f"Rendered: {png_path} ({width}px, {size_kb:.1f} KB)")


# ==============================================================================
# DIAGRAM 1: HOTSTAR END-TO-END PRODUCTION CLOUD ARCHITECTURE (MODERN ERA 3)
# ==============================================================================
def generate_diagram_1():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" width="1440" height="900">
  <defs>
    <marker id="arr-gray" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#475569" />
    </marker>
    <marker id="arr-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284C7" />
    </marker>
    <marker id="arr-emerald" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
    </marker>
    <filter id="c-shadow" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.05"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" fill="#F8FAFC" />

  <!-- Title & Subtitle -->
  <text x="720" y="45" font-family="'Segoe UI', Roboto, sans-serif" font-size="24" font-weight="bold" fill="#0F172A" text-anchor="middle">Hotstar Production Cloud Architecture (Modern Era)</text>
  <text x="720" y="74" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" fill="#475569" text-anchor="middle">End-to-End Scalability Pipeline: Multi-CDN Edge Shield → Ingress ALBs → Envoy Gateway → 6 EKS Clusters → Managed Data Tier</text>

  <!-- COLUMN 1: CLIENT TIER (X: 40, W: 220) -->
  <rect x="40" y="95" width="220" height="770" rx="14" fill="#EEF2FF" stroke="#818CF8" stroke-width="1.8" />
  <rect x="65" y="85" width="170" height="22" rx="4" fill="#4F46E5" />
  <text x="150" y="100" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">HETEROGENEOUS CLIENTS</text>

  <!-- Mobile Card -->
  <g transform="translate(55, 125)" filter="url(#c-shadow)">
    <rect width="190" height="220" rx="8" fill="#FFFFFF" stroke="#C7D2FE" stroke-width="1.2" />
    <rect x="10" y="12" width="80" height="18" rx="3" fill="#4F46E5" />
    <text x="50" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">MOBILE APPS</text>
    <text x="10" y="52" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="bold" fill="#1E1B4B">Android &amp; iOS</text>
    <text x="10" y="80" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• 60M+ Active Viewers</text>
    <text x="10" y="102" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Low-Latency HLS / DASH</text>
    <text x="10" y="124" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• ExoPlayer / AVPlayer</text>
    <text x="10" y="146" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Chunk pre-fetch logic</text>
    <text x="10" y="168" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Client token caching</text>
    <text x="10" y="190" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Telemetry heartbeats</text>
  </g>

  <!-- Web Card -->
  <g transform="translate(55, 370)" filter="url(#c-shadow)">
    <rect width="190" height="220" rx="8" fill="#FFFFFF" stroke="#C7D2FE" stroke-width="1.2" />
    <rect x="10" y="12" width="90" height="18" rx="3" fill="#4F46E5" />
    <text x="55" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">WEB PLATFORM</text>
    <text x="10" y="52" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="bold" fill="#1E1B4B">React Web Player</text>
    <text x="10" y="80" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Desktop browsers</text>
    <text x="10" y="102" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Adaptive bitrate (ABR)</text>
    <text x="10" y="124" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Shaka / Hls.js engine</text>
    <text x="10" y="146" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Lightweight UI bundles</text>
    <text x="10" y="168" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Real-time error reports</text>
    <text x="10" y="190" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• CDN failover routing</text>
  </g>

  <!-- TV Card -->
  <g transform="translate(55, 615)" filter="url(#c-shadow)">
    <rect width="190" height="220" rx="8" fill="#FFFFFF" stroke="#C7D2FE" stroke-width="1.2" />
    <rect x="10" y="12" width="95" height="18" rx="3" fill="#4F46E5" />
    <text x="57" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">LIVING ROOM TV</text>
    <text x="10" y="52" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="bold" fill="#1E1B4B">Connected TV</text>
    <text x="10" y="80" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Android TV / Tizen</text>
    <text x="10" y="102" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Apple TV &amp; FireTV</text>
    <text x="10" y="124" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• 4K HDR Dolby Vision</text>
    <text x="10" y="146" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• High-bitrate streams</text>
    <text x="10" y="168" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Large buffer windows</text>
    <text x="10" y="190" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Low-churn watch state</text>
  </g>

  <!-- Flow 1: Clients to CDN -->
  <path d="M 260 480 L 290 480" fill="none" stroke="#4F46E5" stroke-width="3" marker-end="url(#arr-gray)" />
  <rect x="252" y="468" width="45" height="24" rx="4" fill="#4F46E5" />
  <text x="274" y="484" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">61.2M</text>

  <!-- COLUMN 2: MULTI-CDN EDGE SHIELD (X: 290, W: 250) -->
  <rect x="290" y="95" width="250" height="770" rx="14" fill="#E0F2FE" stroke="#38BDF8" stroke-width="1.8" />
  <rect x="315" y="85" width="200" height="22" rx="4" fill="#0284C7" />
  <text x="415" y="100" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">MULTI-CDN EDGE SHIELD</text>

  <!-- CDN Edge POPs Card -->
  <g transform="translate(305, 125)" filter="url(#c-shadow)">
    <rect width="220" height="390" rx="8" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" />
    <rect x="12" y="12" width="75" height="18" rx="3" fill="#0284C7" />
    <text x="49" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">EDGE POPs</text>
    <text x="12" y="52" font-family="'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="bold" fill="#0369A1">Akamai &amp; CloudFront</text>
    <text x="12" y="82" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0284C7">• 95%+ Cache Offload Ratio</text>
    <text x="12" y="110" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Static Video Chunks (.m4s)</text>
    <text x="12" y="136" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• HLS Master / Media Playlists</text>
    <text x="12" y="162" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Anycast Edge IP Routing</text>
    <text x="12" y="188" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• TLS 1.3 Termination at Edge</text>
    <text x="12" y="214" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• AWS Shield DDoS Protection</text>
    <text x="12" y="240" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Web Application Firewall (WAF)</text>
    <text x="12" y="266" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Geo-fencing &amp; IP Validation</text>
    <text x="12" y="296" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#0284C7">• 25+ Tbps Aggregate Peak</text>
    <text x="12" y="324" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Origin Request Collapsing</text>
    <text x="12" y="350" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Dynamic Origin Failover</text>
  </g>

  <!-- Edge Rate Limiting Card -->
  <g transform="translate(305, 535)" filter="url(#c-shadow)">
    <rect width="220" height="300" rx="8" fill="#FFFFFF" stroke="#BAE6FD" stroke-width="1.2" />
    <rect x="12" y="12" width="80" height="18" rx="3" fill="#0369A1" />
    <text x="52" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">EDGE LOGIC</text>
    <text x="12" y="52" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#0369A1">Edge Rate Limiting</text>
    <text x="12" y="82" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Token Pre-Validation at POP</text>
    <text x="12" y="108" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Bot &amp; Scraper Filtering</text>
    <text x="12" y="134" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Rate Limiting per User IP</text>
    <text x="12" y="160" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Non-cacheable APIs (5%) routed</text>
    <text x="12" y="186" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Direct route to Mumbai ALBs</text>
    <text x="12" y="212" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Dynamic TCP connection reuse</text>
    <text x="12" y="238" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Pre-match static priming</text>
    <text x="12" y="264" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Origin protection shield</text>
  </g>

  <!-- Flow 2: Edge to AWS Region -->
  <path d="M 540 240 L 590 240" fill="none" stroke="#0284C7" stroke-width="3" marker-end="url(#arr-blue)" />
  <rect x="536" y="228" width="55" height="24" rx="4" fill="#0284C7" />
  <text x="563" y="244" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">5% Origin</text>

  <!-- AWS REGION CONTAINER (X: 570, W: 830) -->
  <rect x="570" y="95" width="830" height="770" rx="14" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.8" stroke-dasharray="6 6" />
  <rect x="595" y="85" width="280" height="22" rx="4" fill="#334155" />
  <text x="735" y="100" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">AWS REGION: ap-south-1 (MUMBAI VPC)</text>

  <!-- SUB-COLUMN A: INGRESS & ENVOY MESH (X: 590, W: 220) -->
  <!-- Ingress ALBs Card -->
  <g transform="translate(590, 125)" filter="url(#c-shadow)">
    <rect width="220" height="240" rx="8" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1.5" />
    <rect x="12" y="12" width="85" height="18" rx="3" fill="#16A34A" />
    <text x="54" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">INGRESS TIER</text>
    <text x="12" y="52" font-family="'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="bold" fill="#166534">AWS Ingress ALBs</text>
    <text x="12" y="80" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Route 53 Latency Routing</text>
    <text x="12" y="104" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Cross-Zone Load Balancing</text>
    <text x="12" y="128" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Unified Ingress Entry Point</text>
    <text x="12" y="152" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#16A34A">• Replaced 200+ legacy ALBs</text>
    <text x="12" y="176" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Target Group: Envoy Proxies</text>
    <text x="12" y="200" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Zero ALB Hairpinning Loops</text>
  </g>

  <!-- Flow Ingress to Envoy -->
  <path d="M 700 365 L 700 405" fill="none" stroke="#059669" stroke-width="3" marker-end="url(#arr-emerald)" />

  <!-- Envoy API Gateway Card -->
  <g transform="translate(590, 410)" filter="url(#c-shadow)">
    <rect width="220" height="425" rx="8" fill="#F0FDF4" stroke="#10B981" stroke-width="2" />
    <rect x="12" y="12" width="95" height="18" rx="3" fill="#059669" />
    <text x="59" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">GATEWAY MESH</text>
    <text x="12" y="52" font-family="'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="bold" fill="#065F46">Envoy API Gateway</text>
    <text x="12" y="80" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#059669">• Central Datacenter Router</text>
    <text x="12" y="104" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Dynamic Service Discovery</text>
    <text x="12" y="128" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Resolves Internal VPC Pod IPs</text>
    <text x="12" y="154" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#047857">• Graceful Degradation:</text>
    <text x="20" y="174" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#065F46">"Jettison" Feature Shedding</text>
    <text x="12" y="198" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Slices Non-Critical APIs</text>
    <text x="12" y="222" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Protects Video Playlists</text>
    <text x="12" y="246" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Internal mTLS Encryption</text>
    <text x="12" y="270" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Distributed Tracing (Jaeger)</text>
    <text x="12" y="294" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Active Health Checking</text>
    <text x="12" y="318" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Cluster Load Shedding</text>
    <text x="12" y="342" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• gRPC &amp; HTTP/2 Ingress</text>
  </g>

  <!-- SUB-COLUMN B: 6 EKS CLUSTERS (X: 835, W: 310) -->
  <rect x="835" y="115" width="310" height="720" rx="10" fill="#FFFBEB" stroke="#F59E0B" stroke-width="1.8" />
  <rect x="855" y="105" width="270" height="20" rx="4" fill="#D97706" />
  <text x="990" y="119" font-family="'Segoe UI', Roboto, sans-serif" font-size="9.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">6 MANAGED AMAZON EKS CLUSTERS</text>

  <!-- Tier 1 Cluster -->
  <g transform="translate(850, 135)" filter="url(#c-shadow)">
    <rect width="280" height="210" rx="8" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.2" />
    <rect x="12" y="12" width="130" height="18" rx="3" fill="#D97706" />
    <text x="77" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="8" font-weight="bold" fill="#FFFFFF" text-anchor="middle">TIER-1 (ISOLATED CLUSTER)</text>
    <text x="12" y="48" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#B45309">Streaming Origin Core</text>
    <text x="12" y="74" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Live Playlist &amp; Manifest API</text>
    <text x="12" y="96" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Player Token &amp; Entitlement</text>
    <text x="12" y="120" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#D97706">• 100% Guaranteed Origin Compute</text>
    <text x="12" y="144" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Zero sharing with non-critical pods</text>
    <text x="12" y="166" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Multi-AZ Pod Anti-Affinity</text>
  </g>

  <!-- Tier 2 Cluster -->
  <g transform="translate(850, 365)" filter="url(#c-shadow)">
    <rect width="280" height="200" rx="8" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.2" />
    <rect x="12" y="12" width="135" height="18" rx="3" fill="#B45309" />
    <text x="79" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="8" font-weight="bold" fill="#FFFFFF" text-anchor="middle">TIER-2 (PLATFORM CLUSTERS)</text>
    <text x="12" y="48" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#B45309">Catalog &amp; Watch APIs</text>
    <text x="12" y="74" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Content Discovery &amp; Search API</text>
    <text x="12" y="96" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• User Profiles &amp; Watch History</text>
    <text x="12" y="118" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Device Session Management</text>
    <text x="12" y="140" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• AWS VPC CNI on /19 Subnets</text>
    <text x="12" y="162" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• 8,190 IP Addresses per Subnet</text>
  </g>

  <!-- Tier 3 Cluster -->
  <g transform="translate(850, 585)" filter="url(#c-shadow)">
    <rect width="280" height="230" rx="8" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.2" />
    <rect x="12" y="12" width="135" height="18" rx="3" fill="#92400E" />
    <text x="79" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="8" font-weight="bold" fill="#FFFFFF" text-anchor="middle">TIER-3 (SHEDDABLE CLUSTERS)</text>
    <text x="12" y="48" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#B45309">Interactive Social Engine</text>
    <text x="12" y="74" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Real-time Cricket Scores &amp; Stats</text>
    <text x="12" y="96" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Live Comments &amp; Emoji Feeds</text>
    <text x="12" y="118" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Interactive Polls &amp; Quiz Engine</text>
    <text x="12" y="140" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#DC2626">• Shed programmatically during spikes</text>
    <text x="12" y="164" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Karpenter Node Autoscaler</text>
    <text x="12" y="186" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• EC2 Spot Fleet (70% savings)</text>
    <text x="12" y="208" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Sub-minute node spinup</text>
  </g>

  <!-- Flow Envoy to Clusters -->
  <path d="M 810 240 L 850 240" fill="none" stroke="#059669" stroke-width="2.5" marker-end="url(#arr-emerald)" />
  <path d="M 810 465 L 850 465" fill="none" stroke="#059669" stroke-width="2.5" marker-end="url(#arr-emerald)" />
  <path d="M 810 670 L 850 670" fill="none" stroke="#059669" stroke-width="2.5" marker-end="url(#arr-emerald)" />

  <!-- SUB-COLUMN C: MANAGED DATA TIER (X: 1170, W: 210) -->
  <rect x="1170" y="115" width="210" height="720" rx="10" fill="#F5F3FF" stroke="#C4B5FD" stroke-width="1.8" />
  <rect x="1190" y="105" width="170" height="20" rx="4" fill="#7C3AED" />
  <text x="1275" y="119" font-family="'Segoe UI', Roboto, sans-serif" font-size="9.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">MANAGED DATA TIER</text>

  <!-- Aurora Postgres Card -->
  <g transform="translate(1185, 135)" filter="url(#c-shadow)">
    <rect width="180" height="160" rx="8" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="1.2" />
    <rect x="10" y="12" width="70" height="18" rx="3" fill="#7C3AED" />
    <text x="45" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">RELATIONAL</text>
    <text x="10" y="48" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5" font-weight="bold" fill="#5B21B6">Aurora Postgres</text>
    <text x="10" y="74" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Multi-AZ Cluster</text>
    <text x="10" y="96" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Read Replicas</text>
    <text x="10" y="118" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Subscription DB</text>
  </g>

  <!-- DynamoDB Card -->
  <g transform="translate(1185, 315)" filter="url(#c-shadow)">
    <rect width="180" height="160" rx="8" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="1.2" />
    <rect x="10" y="12" width="60" height="18" rx="3" fill="#7C3AED" />
    <text x="40" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">NO-SQL</text>
    <text x="10" y="48" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5" font-weight="bold" fill="#5B21B6">DynamoDB</text>
    <text x="10" y="74" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Session Storage</text>
    <text x="10" y="96" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Auto-scaled RCU/WCU</text>
    <text x="10" y="118" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Single-digit ms reads</text>
  </g>

  <!-- ElastiCache Redis Card -->
  <g transform="translate(1185, 495)" filter="url(#c-shadow)">
    <rect width="180" height="160" rx="8" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="1.2" />
    <rect x="10" y="12" width="70" height="18" rx="3" fill="#7C3AED" />
    <text x="45" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">IN-MEMORY</text>
    <text x="10" y="48" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5" font-weight="bold" fill="#5B21B6">ElastiCache Redis</text>
    <text x="10" y="74" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Sub-ms Metadata Cache</text>
    <text x="10" y="96" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Cluster Sharding</text>
    <text x="10" y="118" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Read Replicas per AZ</text>
  </g>

  <!-- Kafka & S3 Origin Card -->
  <g transform="translate(1185, 675)" filter="url(#c-shadow)">
    <rect width="180" height="145" rx="8" fill="#FFFFFF" stroke="#DDD6FE" stroke-width="1.2" />
    <rect x="10" y="10" width="115" height="18" rx="3" fill="#7C3AED" />
    <text x="67" y="22" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">STREAM &amp; STORAGE</text>
    <text x="10" y="46" font-family="'Segoe UI', Roboto, sans-serif" font-size="13.5" font-weight="bold" fill="#5B21B6">Kafka &amp; S3 Origin</text>
    <text x="10" y="70" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• MSK Telemetry Streams</text>
    <text x="10" y="92" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Millions of events/sec</text>
    <text x="10" y="114" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• S3 Video Master Storage</text>
  </g>

  <!-- Flow Clusters to Data Tier -->
  <path d="M 1145 480 L 1170 480" fill="none" stroke="#7C3AED" stroke-width="3" marker-end="url(#arr-gray)" />

</svg>"""
    render_svg(svg, "hotstar_high_level_architecture.png")


# ==============================================================================
# DIAGRAM 2: ERA 2 BOTTLENECK: SERVICE-TO-SERVICE HAIRPINNING (PERFECT CLEARANCE)
# ==============================================================================
def generate_diagram_2():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" width="1440" height="900">
  <defs>
    <marker id="arr-red" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#DC2626" />
    </marker>
    <filter id="c-shadow-2" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.05"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" fill="#F8FAFC" />

  <!-- Title & Subtitle -->
  <text x="720" y="42" font-family="'Segoe UI', Roboto, sans-serif" font-size="24" font-weight="bold" fill="#991B1B" text-anchor="middle">Era 2 Architectural Bottleneck: Service-to-Service Hairpinning</text>
  <text x="720" y="68" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" fill="#475569" text-anchor="middle">Legacy Topology (2019–2022): Self-Managed Kubernetes with Route 53 &amp; External Application Load Balancer Loops</text>

  <!-- TOP LAYER: PUBLIC INTERNET & EXTERNAL ALB TIER (Y: 95 to 235) -->
  <rect x="50" y="95" width="1340" height="140" rx="14" fill="#FEF2F2" stroke="#F87171" stroke-width="2" stroke-dasharray="6 6" />
  <rect x="75" y="85" width="460" height="22" rx="4" fill="#DC2626" />
  <text x="305" y="100" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">PUBLIC INTERNET &amp; EXTERNAL ROUTE 53 / APPLICATION LOAD BALANCER TIER</text>

  <!-- Top Card 1: service-a ALB (Left: X: 80, W: 360) -->
  <g transform="translate(80, 115)" filter="url(#c-shadow-2)">
    <rect width="360" height="105" rx="8" fill="#FFFFFF" stroke="#FCA5A5" stroke-width="1.5" />
    <rect x="14" y="10" width="85" height="18" rx="3" fill="#DC2626" />
    <text x="56" y="23" font-family="'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">ALB POOL 1</text>
    <text x="110" y="25" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#0F172A">service-a.hotstar.com</text>
    <text x="14" y="54" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#475569">• External Application Load Balancer</text>
    <text x="14" y="74" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#475569">• Public DNS resolved via AWS Route 53</text>
    <text x="14" y="94" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#DC2626">• Target of hairpin loop from Cluster 1</text>
  </g>

  <!-- Top Center Box: Hairpin Explanation (X: 480, W: 480) -->
  <g transform="translate(480, 115)" filter="url(#c-shadow-2)">
    <rect width="480" height="105" rx="8" fill="#FFFFFF" stroke="#F87171" stroke-width="1.8" />
    <rect x="14" y="10" width="165" height="18" rx="3" fill="#991B1B" />
    <text x="96" y="23" font-family="'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">HAIRPIN FAILURE MODE</text>
    <text x="190" y="25" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="bold" fill="#991B1B">Cross-Cluster RPC Leaves VPC!</text>
    <text x="14" y="54" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#7F1D1D">• Service B calls public DNS rather than direct pod IPs</text>
    <text x="14" y="74" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#7F1D1D">• Packets exit VPC via NAT Gateway, traverse public Internet</text>
    <text x="14" y="94" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#DC2626">• Re-enters via NodePort, adding 150ms+ tail latency</text>
  </g>

  <!-- Top Card 3: 200+ ALBs Overhead (Right: X: 1000, W: 360) -->
  <g transform="translate(1000, 115)" filter="url(#c-shadow-2)">
    <rect width="360" height="105" rx="8" fill="#FFFFFF" stroke="#FCA5A5" stroke-width="1.5" />
    <rect x="14" y="10" width="135" height="18" rx="3" fill="#991B1B" />
    <text x="81" y="23" font-family="'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">FLEET OVERHEAD</text>
    <text x="160" y="25" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="bold" fill="#991B1B">200+ Dedicated ALBs</text>
    <text x="14" y="54" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#7F1D1D">• Required manual pre-warming tickets</text>
    <text x="14" y="74" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#7F1D1D">• Massive cross-AZ data transfer fees</text>
    <text x="14" y="94" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#7F1D1D">• AWS API rate throttling during spikes</text>
  </g>

  <!-- BOTTOM LAYER: VPC BOUNDARY (Y: 300 to 770) -->
  <rect x="50" y="300" width="1340" height="470" rx="14" fill="#FFFFFF" stroke="#94A3B8" stroke-width="2" />
  <rect x="75" y="290" width="410" height="22" rx="4" fill="#334155" />
  <text x="280" y="305" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">AWS REGION: ap-south-1 (MUMBAI) — PRIVATE VPC BOUNDARY</text>

  <!-- Cluster 1 Box (Left: X: 80, W: 610) -->
  <g transform="translate(80, 325)">
    <rect width="610" height="425" rx="12" fill="#FFFBEB" stroke="#F59E0B" stroke-width="1.8" />
    <rect x="25" y="14" width="280" height="22" rx="4" fill="#B45309" />
    <text x="165" y="29" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">KUBERNETES CLUSTER 1 (Self-Managed)</text>

    <!-- Service B Card -->
    <g transform="translate(25, 48)" filter="url(#c-shadow-2)">
      <rect width="560" height="175" rx="8" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.5" />
      <rect x="14" y="14" width="120" height="22" rx="4" fill="#D97706" />
      <text x="74" y="29" font-family="'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle">CALLER SERVICE</text>
      <text x="145" y="31" font-family="'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="bold" fill="#0F172A">Service B (Watch Session Service)</text>
      <text x="14" y="68" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">• Manages live user streaming sessions and player heartbeats</text>
      <text x="14" y="90" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">• Needs user entitlement and catalog metadata from Service A</text>
      <text x="14" y="112" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#DC2626">• Cannot resolve pod IPs across cluster boundaries directly</text>
      <text x="14" y="134" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#DC2626">• Dispatches external HTTP call out to service-a.hotstar.com</text>
      <text x="14" y="156" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#475569">• Incurs outbound NAT Gateway transit and TLS handshakes</text>
    </g>

    <!-- NodePort Worker Nodes Card -->
    <g transform="translate(25, 235)" filter="url(#c-shadow-2)">
      <rect width="560" height="175" rx="8" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.5" />
      <rect x="14" y="14" width="115" height="22" rx="4" fill="#B45309" />
      <text x="71" y="29" font-family="'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle">WORKER NODES</text>
      <text x="140" y="31" font-family="'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="bold" fill="#0F172A">NodePort Range: 30000–32767</text>
      <text x="14" y="68" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">• Fixed range of only 2,767 usable ports across the entire cluster fleet</text>
      <text x="14" y="90" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">• Port collisions as services scaled up; Target Groups mapped to NodePorts</text>
      <text x="14" y="112" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">• AWS VPC subnet IP exhaustion under rapid container launches (/24 subnets)</text>
      <text x="14" y="134" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#B45309">• Inefficient kube-proxy iptables rule table with thousands of routes</text>
      <text x="14" y="156" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#B45309">• NodePort exposed node IPs directly to public VPC routing tables</text>
    </g>
  </g>

  <!-- Cluster 2 Box (Right: X: 750, W: 610) -->
  <g transform="translate(750, 325)">
    <rect width="610" height="425" rx="12" fill="#FFFBEB" stroke="#F59E0B" stroke-width="1.8" />
    <rect x="25" y="14" width="280" height="22" rx="4" fill="#B45309" />
    <text x="165" y="29" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">KUBERNETES CLUSTER 2 (Self-Managed)</text>

    <!-- Service A Card -->
    <g transform="translate(25, 48)" filter="url(#c-shadow-2)">
      <rect width="560" height="175" rx="8" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.5" />
      <rect x="14" y="14" width="130" height="22" rx="4" fill="#D97706" />
      <text x="79" y="29" font-family="'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle">RECEIVER SERVICE</text>
      <text x="155" y="31" font-family="'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="bold" fill="#0F172A">Service A (Entitlement / Catalog API)</text>
      <text x="14" y="68" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">• Validates subscription status, stream tokens, and device entitlements</text>
      <text x="14" y="90" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">• Receives internal calls via external public ALB ingress!</text>
      <text x="14" y="112" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#DC2626">• Re-encrypts and re-negotiates TLS on every internal service hop</text>
      <text x="14" y="134" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#DC2626">• Doubles origin latency and subjects internal RPCs to public DNS TTLs</text>
      <text x="14" y="156" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#475569">• Target Group connection limits throttled peak cricket bursts</text>
    </g>

    <!-- Control Plane Card -->
    <g transform="translate(25, 235)" filter="url(#c-shadow-2)">
      <rect width="560" height="175" rx="8" fill="#FFFFFF" stroke="#FDE68A" stroke-width="1.5" />
      <rect x="14" y="14" width="130" height="22" rx="4" fill="#B45309" />
      <text x="79" y="29" font-family="'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle">CONTROL PLANE</text>
      <text x="155" y="31" font-family="'Segoe UI', Roboto, sans-serif" font-size="15" font-weight="bold" fill="#0F172A">kube-apiserver &amp; etcd Contention</text>
      <text x="14" y="68" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">• Two large clusters hosting hundreds of microservices simultaneously</text>
      <text x="14" y="90" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">• High churn during spikes caused etcd leader election timeouts and raft lag</text>
      <text x="14" y="112" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#334155">• Lack of failure domain isolation: crash in one service affected entire cluster</text>
      <text x="14" y="134" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#B45309">• Legacy Kubernetes 1.17 could not run Karpenter or modern VPC CNI</text>
      <text x="14" y="156" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" fill="#B45309">• Master node scaling took hours, unable to adapt to sudden cricket spikes</text>
    </g>
  </g>

  <!-- HAIRPIN ROUTING: CLEAN ORTHOGONAL PATHWAYS THROUGH OPEN GAP (Y: 240 to 290) -->
  <!-- Step 1: Upward arrow from Service B (Cluster 1) to ALB Pool 1 -->
  <path d="M 380 373 L 380 225" fill="none" stroke="#DC2626" stroke-width="3.5" marker-end="url(#arr-red)" />
  <rect x="240" y="250" width="280" height="24" rx="4" fill="#DC2626" />
  <text x="380" y="266" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">1. Outbound RPC to service-a.hotstar.com</text>

  <!-- Step 2: The Hairpin Loop from ALB Pool 1, down through open gap, across to Cluster 2, and into Service A -->
  <!-- Exits ALB at (430, 220), drops to Y=268 in open gap, runs horizontally to X=1180, then drops to Service A at Y=373 -->
  <!-- (At X=1180 in Cluster 2, there is zero header text, providing a 100% clean vertical drop!) -->
  <path d="M 430 220 L 430 268 L 1180 268 L 1180 368" fill="none" stroke="#DC2626" stroke-width="4" stroke-dasharray="8 6" marker-end="url(#arr-red)" />
  
  <!-- Step 2 Badge placed cleanly on the horizontal line in the open gap -->
  <rect x="670" y="256" width="200" height="25" rx="4" fill="#DC2626" />
  <text x="770" y="273" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">2. THE HAIRPIN LOOP</text>

  <!-- BOTTOM CALLOUT BANNER (Y: 790 to 875) -->
  <g transform="translate(50, 790)" filter="url(#c-shadow-2)">
    <rect width="1340" height="85" rx="10" fill="#FEF2F2" stroke="#DC2626" stroke-width="2" />
    <rect x="18" y="18" width="135" height="50" rx="6" fill="#DC2626" />
    <text x="85" y="38" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">SYSTEMIC</text>
    <text x="85" y="55" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">IMPACT</text>
    <text x="175" y="38" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#991B1B">• Severe Tail Latency Amplification: Each internal RPC incurred Route 53 DNS lookup, external TLS handshake, and extra network hops.</text>
    <text x="175" y="60" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#991B1B">• Operational Fragility: 200+ ALBs required manual pre-warming tickets with AWS support before every major tournament.</text>
  </g>
</svg>"""
    render_svg(svg, "hotstar_service_hairpinning_bottleneck.png")


# ==============================================================================
# DIAGRAM 3: ERA 3 ARCHITECTURE: DATACENTER ABSTRACTION & ENVOY GATEWAY MESH
# ==============================================================================
def generate_diagram_3():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" width="1440" height="900">
  <defs>
    <marker id="arr-em-3" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#059669" />
    </marker>
    <marker id="arr-blue-3" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284C7" />
    </marker>
    <filter id="c-shadow-3" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.05"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" fill="#F8FAFC" />

  <!-- Title & Subtitle -->
  <text x="720" y="42" font-family="'Segoe UI', Roboto, sans-serif" font-size="24" font-weight="bold" fill="#065F46" text-anchor="middle">Era 3 Architecture: Datacenter Abstraction &amp; Envoy Gateway Mesh</text>
  <text x="720" y="68" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" fill="#475569" text-anchor="middle">Modern Solution (2023–Present): Unified Ingress, Internal Envoy Service Discovery, Multi-Cluster Cell Isolation &amp; Zero ALB Hairpinning</text>

  <!-- TOP INGRESS STRIP (Y: 90 to 220) -->
  <rect x="50" y="90" width="1340" height="130" rx="14" fill="#FFFFFF" stroke="#94A3B8" stroke-width="1.8" />
  <rect x="75" y="80" width="340" height="22" rx="4" fill="#334155" />
  <text x="245" y="95" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">PUBLIC EDGE &amp; UNIFIED INGRESS TIER</text>

  <!-- Box 1: Global Viewers -->
  <g transform="translate(75, 105)" filter="url(#c-shadow-3)">
    <rect width="320" height="95" rx="8" fill="#EEF2FF" stroke="#C7D2FE" stroke-width="1.2" />
    <rect x="12" y="10" width="100" height="18" rx="3" fill="#4F46E5" />
    <text x="62" y="22" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">CLIENT INGRESS</text>
    <text x="12" y="46" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#1E1B4B">Global Viewers (60M+)</text>
    <text x="12" y="68" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Multi-CDN Shield &amp; Anycast Edge</text>
    <text x="12" y="86" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Dynamic Origin Request Routing</text>
  </g>

  <!-- Arrow 1 to 2 -->
  <path d="M 395 152 L 455 152" fill="none" stroke="#4F46E5" stroke-width="3" marker-end="url(#arr-blue-3)" />

  <!-- Box 2: Unified Ingress ALBs -->
  <g transform="translate(455, 105)" filter="url(#c-shadow-3)">
    <rect width="350" height="95" rx="8" fill="#F0F9FF" stroke="#BAE6FD" stroke-width="1.2" />
    <rect x="12" y="10" width="115" height="18" rx="3" fill="#0284C7" />
    <text x="69" y="22" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">CONSOLIDATED</text>
    <text x="12" y="46" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#0369A1">Unified Ingress ALBs</text>
    <text x="12" y="68" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Replaced 200+ legacy public ALBs</text>
    <text x="12" y="86" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Ingress only: zero internal RPC traffic</text>
  </g>

  <!-- Arrow 2 to 3 -->
  <path d="M 805 152 L 865 152" fill="none" stroke="#0284C7" stroke-width="3" marker-end="url(#arr-em-3)" />

  <!-- Box 3: Envoy API Gateway Mesh -->
  <g transform="translate(865, 105)" filter="url(#c-shadow-3)">
    <rect width="500" height="95" rx="8" fill="#F0FDF4" stroke="#86EFAC" stroke-width="1.5" />
    <rect x="12" y="10" width="115" height="18" rx="3" fill="#059669" />
    <text x="69" y="22" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">GATEWAY MESH</text>
    <text x="12" y="46" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#065F46">Envoy API Gateway (Central Datacenter Router)</text>
    <text x="12" y="68" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Dynamic xDS discovery &amp; internal routing to 6 EKS clusters</text>
    <text x="12" y="86" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• "Jettison" automated feature-shedding under peak cricket traffic</text>
  </g>

  <!-- MIDDLE CONTAINER: LOGICAL DATACENTER ABSTRACTION (Y: 245 to 770) -->
  <rect x="50" y="245" width="1340" height="525" rx="14" fill="#F0FDF4" stroke="#10B981" stroke-width="2" />
  <rect x="75" y="235" width="620" height="22" rx="4" fill="#059669" />
  <text x="385" y="250" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">LOGICAL DATACENTER ABSTRACTION (6 Managed EKS Clusters in Mumbai Treated as One Fabric)</text>

  <!-- Clean Distribution from Envoy into Clusters: Two dedicated vertical drops with ZERO text collisions -->
  <!-- Drop to Cluster 1: Exits Envoy at X: 890, drops through top border (where there is no badge) to Y: 270 (below badge), travels left to X: 480, drops cleanly into Cluster 1 -->
  <path d="M 890 200 L 890 270 L 480 270 L 480 295" fill="none" stroke="#059669" stroke-width="2.5" marker-end="url(#arr-em-3)" />

  <!-- Drop to Cluster 2: Exits Envoy at X: 1180, drops straight down at X: 1180 into Cluster 2 -->
  <path d="M 1180 200 L 1180 295" fill="none" stroke="#059669" stroke-width="2.5" marker-end="url(#arr-em-3)" />

  <!-- Cluster 1 (Left: X: 80, W: 570) -->
  <g transform="translate(80, 295)">
    <rect width="570" height="455" rx="12" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1.8" />
    <rect x="25" y="14" width="260" height="22" rx="4" fill="#059669" />
    <text x="155" y="29" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">AMAZON EKS CLUSTER 1 (Managed)</text>

    <!-- Service B Card -->
    <g transform="translate(25, 50)" filter="url(#c-shadow-3)">
      <rect width="520" height="175" rx="8" fill="#F0FDF4" stroke="#A7F3D0" stroke-width="1.5" />
      <rect x="14" y="12" width="120" height="20" rx="3" fill="#059669" />
      <text x="74" y="26" font-family="'Segoe UI', Roboto, sans-serif" font-size="9.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">CALLER SERVICE</text>
      <text x="145" y="28" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#065F46">Service B (Watch Session Service)</text>
      <text x="14" y="62" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Manages live user streaming heartbeats and concurrency counters</text>
      <text x="14" y="84" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Requires instant entitlement checks and catalog metadata from Service A</text>
      <text x="14" y="106" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#059669">• Resolved via Envoy Internal Mesh: Private ClusterIP resolution</text>
      <text x="14" y="128" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#059669">• Packets STAY INSIDE VPC — Zero Route 53 lookups, Zero ALB hops</text>
      <text x="14" y="150" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#065F46">• Internal latency reduced from ~150ms to sub-2 milliseconds!</text>
    </g>

    <!-- Networking Infrastructure Card -->
    <g transform="translate(25, 245)" filter="url(#c-shadow-3)">
      <rect width="520" height="185" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" />
      <rect x="14" y="12" width="130" height="20" rx="3" fill="#334155" />
      <text x="79" y="26" font-family="'Segoe UI', Roboto, sans-serif" font-size="9.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">NETWORKING CORE</text>
      <text x="155" y="28" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#0F172A">AWS VPC CNI on /19 Subnets</text>
      <text x="14" y="62" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• 8,190 usable private IP addresses per subnet (zero IP exhaustion)</text>
      <text x="14" y="84" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Elastic Network Interfaces (ENIs) attached directly to EC2 Nitro instances</text>
      <text x="14" y="106" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Per-subnet NAT Gateways prevent cross-AZ bottleneck and data transfer costs</text>
      <text x="14" y="128" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Eliminates legacy NodePort mapping and avoids iptables rule saturation</text>
      <text x="14" y="150" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#059669">• Pod-to-pod communication flows natively across VPC private routes</text>
    </g>
  </g>

  <!-- Cluster 2 (Right: X: 790, W: 570) -->
  <g transform="translate(790, 295)">
    <rect width="570" height="455" rx="12" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1.8" />
    <rect x="25" y="14" width="260" height="22" rx="4" fill="#059669" />
    <text x="155" y="29" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#FFFFFF" text-anchor="middle">AMAZON EKS CLUSTER 2 (Managed)</text>

    <!-- Service A Card -->
    <g transform="translate(25, 50)" filter="url(#c-shadow-3)">
      <rect width="520" height="175" rx="8" fill="#F0FDF4" stroke="#A7F3D0" stroke-width="1.5" />
      <rect x="14" y="12" width="135" height="20" rx="3" fill="#059669" />
      <text x="81" y="26" font-family="'Segoe UI', Roboto, sans-serif" font-size="9.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">RECEIVER SERVICE</text>
      <text x="160" y="28" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#065F46">Service A (Entitlement / Catalog API)</text>
      <text x="14" y="62" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Receives internal calls directly over private ClusterIP mesh</text>
      <text x="14" y="84" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Mutual TLS (mTLS) handshake handled transparently via Envoy sidecars</text>
      <text x="14" y="106" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#059669">• Completely isolated failure domain: Cluster 2 issues never crash Cluster 1</text>
      <text x="14" y="128" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Backed by high-throughput ElastiCache Redis replication ring</text>
      <text x="14" y="150" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#065F46">• Protected by Envoy localized circuit breaking and rate limiting</text>
    </g>

    <!-- Node Elasticity Card -->
    <g transform="translate(25, 245)" filter="url(#c-shadow-3)">
      <rect width="520" height="185" rx="8" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.5" />
      <rect x="14" y="12" width="135" height="20" rx="3" fill="#334155" />
      <text x="81" y="26" font-family="'Segoe UI', Roboto, sans-serif" font-size="9.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">NODE ELASTICITY</text>
      <text x="160" y="28" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#0F172A">Karpenter High-Velocity Autoscaler</text>
      <text x="14" y="62" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Directly provisions right-sized EC2 instances in under 45 seconds</text>
      <text x="14" y="84" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Replaced legacy Cluster Autoscaler which suffered from 10-15 minute lag</text>
      <text x="14" y="106" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Diversified across Spot &amp; On-Demand EC2 instance types (c5, m5, r5)</text>
      <text x="14" y="128" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Automated node consolidation and graceful bin-packing when load subsides</text>
      <text x="14" y="150" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#059669">• Handles explosive IPL cricket traffic surges without pre-warming tickets</text>
    </g>
  </g>

  <!-- DIRECT INTERNAL VPC CALL CONNECTOR IN OPEN AISLE (X: 650 to 790, 140px wide aisle) -->
  <path d="M 625 425 L 815 425" fill="none" stroke="#059669" stroke-width="4" marker-end="url(#arr-em-3)" />
  <rect x="650" y="390" width="140" height="40" rx="6" fill="#059669" />
  <text x="720" y="407" font-family="'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">DIRECT INTERNAL RPC</text>
  <text x="720" y="422" font-family="'Segoe UI', Roboto, sans-serif" font-size="8" fill="#FFFFFF" text-anchor="middle">(Zero ALB Hairpinning)</text>

  <!-- BOTTOM CALLOUT BANNER (Y: 790 to 875) -->
  <g transform="translate(50, 790)" filter="url(#c-shadow-3)">
    <rect width="1340" height="85" rx="10" fill="#ECFDF5" stroke="#059669" stroke-width="2" />
    <rect x="18" y="18" width="135" height="50" rx="6" fill="#059669" />
    <text x="85" y="38" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">ARCHITECTURAL</text>
    <text x="85" y="55" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">TRIUMPH</text>
    <text x="175" y="38" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#065F46">• 98.7% Origin Tail Latency Reduction: Internal RPCs avoid external public ALBs entirely, keeping latency strictly under 2ms.</text>
    <text x="175" y="60" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#065F46">• Cell-Based Resilience: 6 isolated EKS clusters isolate blast radiuses; catastrophic failure in interactive features never affects video playback.</text>
  </g>
</svg>"""
    render_svg(svg, "hotstar_datacenter_abstraction_envoy.png")


# ==============================================================================
# DIAGRAM 4: POC AWS SCALABILITY ARCHITECTURE (100% UNCLUTTERED ORTHOGONAL)
# ==============================================================================
def generate_diagram_4():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" width="1440" height="900">
  <defs>
    <marker id="arr-purple-4" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#4F46E5" />
    </marker>
    <marker id="arr-blue-4" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#0284C7" />
    </marker>
    <marker id="arr-red-4" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 1 L 10 5 L 0 9 z" fill="#DC2626" />
    </marker>
    <filter id="c-shadow-4" x="-3%" y="-3%" width="106%" height="106%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.05"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="100%" height="100%" fill="#F8FAFC" />

  <!-- Title & Subtitle -->
  <text x="720" y="42" font-family="'Segoe UI', Roboto, sans-serif" font-size="24" font-weight="bold" fill="#0F172A" text-anchor="middle">IT457 Proof of Concept: Multi-AZ AWS Scalability Architecture</text>
  <text x="720" y="68" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" fill="#475569" text-anchor="middle">Theme 1: Automated Horizontal Elasticity (Locust Swarm → ALB → Multi-AZ ASG with CloudWatch Metric Alarms)</text>

  <!-- LEFT COLUMN: TRAFFIC GENERATOR (X: 45, W: 235) -->
  <rect x="45" y="95" width="235" height="675" rx="14" fill="#EEF2FF" stroke="#818CF8" stroke-width="1.8" />
  <rect x="65" y="85" width="195" height="22" rx="4" fill="#4F46E5" />
  <text x="162" y="100" font-family="'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle">TRAFFIC GENERATION ENGINE</text>

  <!-- Locust Card -->
  <g transform="translate(58, 120)" filter="url(#c-shadow-4)">
    <rect width="210" height="425" rx="8" fill="#FFFFFF" stroke="#C7D2FE" stroke-width="1.5" />
    <rect x="12" y="12" width="120" height="20" rx="3" fill="#4F46E5" />
    <text x="72" y="26" font-family="'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">LOCUST LOAD SWARM</text>
    <text x="12" y="55" font-family="'Segoe UI', Roboto, sans-serif" font-size="16" font-weight="bold" fill="#1E1B4B">Distributed Load</text>
    <text x="12" y="85" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#4F46E5">• Up to 250 Concurrent Users</text>
    <text x="12" y="110" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Hatch Rate: 20 users / second</text>
    <text x="12" y="135" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Headless execution mode</text>
    <text x="12" y="165" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#4F46E5">• Synthetic Workload Endpoints:</text>
    <text x="20" y="190" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">GET /work (Weight: 8)</text>
    <text x="20" y="210" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#475569">2,000 CPU math iterations</text>
    <text x="20" y="235" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0F172A">GET /health (Weight: 2)</text>
    <text x="20" y="255" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#475569">Instant sub-ms heartbeat</text>
    <text x="12" y="290" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="bold" fill="#4F46E5">• Empirical Test Run:</text>
    <text x="20" y="315" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">Total Requests: 55,910</text>
    <text x="20" y="335" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">Zero 5xx Failures (0.00%)</text>
    <text x="20" y="355" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">Peak Throughput: 138 req/s</text>
    <text x="12" y="388" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#475569">• Emulates Hotstar match start spike</text>
  </g>

  <!-- Locust Metrics Callout -->
  <g transform="translate(58, 565)" filter="url(#c-shadow-4)">
    <rect width="210" height="185" rx="8" fill="#F8FAFC" stroke="#C7D2FE" stroke-width="1.2" />
    <text x="105" y="26" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#1E1B4B" text-anchor="middle">EMPIRICAL OUTCOMES</text>
    <text x="14" y="55" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Cold Start: 1 instance @ 95% CPU</text>
    <text x="14" y="78" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Initial Latency: 1,200ms</text>
    <text x="14" y="102" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#059669">• ASG Scaled to 4 Instances</text>
    <text x="14" y="126" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#059669">• Expanded Latency: 46ms median</text>
    <text x="14" y="150" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Latency Drop: 96.2% reduction</text>
  </g>

  <!-- Flow 1: Locust to ALB (Pure 70px open gap between X: 280 and X: 350) -->
  <path d="M 280 195 L 350 195" fill="none" stroke="#4F46E5" stroke-width="3.5" marker-end="url(#arr-purple-4)" />
  <rect x="284" y="166" width="62" height="20" rx="3" fill="#4F46E5" />
  <text x="315" y="180" font-family="'Segoe UI', Roboto, sans-serif" font-size="8" font-weight="bold" fill="#FFFFFF" text-anchor="middle">HTTP/250U</text>

  <!-- RIGHT BIG CONTAINER: AWS REGION VPC (X: 350, W: 1045) -->
  <rect x="350" y="95" width="1045" height="675" rx="14" fill="#FFFFFF" stroke="#94A3B8" stroke-width="2" />
  <rect x="375" y="85" width="460" height="22" rx="4" fill="#334155" />
  <text x="605" y="100" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">AWS REGION: ap-south-1 (MUMBAI) — VPC 10.0.0.0/16 (DUAL-AZ)</text>

  <!-- TOP-LEFT: APPLICATION LOAD BALANCER (X: 370, W: 330, H: 160) -->
  <g transform="translate(370, 115)" filter="url(#c-shadow-4)">
    <rect width="330" height="160" rx="8" fill="#F0F9FF" stroke="#0284C7" stroke-width="2" />
    <rect x="14" y="10" width="110" height="20" rx="4" fill="#0284C7" />
    <text x="69" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">PUBLIC INGRESS</text>
    <text x="135" y="26" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#0369A1">Application Load Balancer</text>
    <text x="14" y="54" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• DNS: hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com</text>
    <text x="14" y="74" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Port 80 HTTP Ingress with Cross-Zone Load Balancing</text>
    <text x="14" y="94" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Target Group: Round-robin to healthy EC2 instances</text>
    <text x="14" y="114" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" fill="#334155">• Health Check: GET /health (15s interval, 2 healthy / 2 unhealthy)</text>
    <text x="14" y="134" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="bold" fill="#0284C7">• Deregistration Delay: 30s connection draining</text>
  </g>

  <!-- TOP-RIGHT: CLOUDWATCH TELEMETRY & ALARMS (X: 720, W: 655, H: 160) -->
  <g transform="translate(720, 115)" filter="url(#c-shadow-4)">
    <rect width="655" height="160" rx="8" fill="#FEF2F2" stroke="#DC2626" stroke-width="2" />
    <rect x="14" y="10" width="150" height="20" rx="4" fill="#DC2626" />
    <text x="89" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">TELEMETRY &amp; ALARMS</text>
    <text x="175" y="26" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#991B1B">AWS CloudWatch Metric Alarms</text>

    <!-- Scale-Out Alarm Box -->
    <rect x="14" y="42" width="305" height="106" rx="6" fill="#FFFFFF" stroke="#FCA5A5" stroke-width="1.2" />
    <text x="24" y="63" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#DC2626">Scale-Out Alarm: CPU &gt;= 50%</text>
    <text x="24" y="83" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Period: 1 minute (1 consecutive evaluation)</text>
    <text x="24" y="103" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Action: Add 1-2 instances immediately</text>
    <text x="24" y="123" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="bold" fill="#DC2626">• Rationale: Headroom before 100% saturation</text>

    <!-- Scale-In Alarm Box -->
    <rect x="335" y="42" width="305" height="106" rx="6" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="1.2" />
    <text x="345" y="63" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#334155">Scale-In Alarm: CPU &lt;= 20%</text>
    <text x="345" y="83" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Period: 3 consecutive evaluations (3 min)</text>
    <text x="345" y="103" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#334155">• Action: Drop capacity back towards Min=1</text>
    <text x="345" y="123" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" fill="#475569">• Cooldown: 300s to avoid flapping</text>
  </g>

  <!-- LOWER CONTAINER: AUTO SCALING GROUP (Y: 330 to 750) -->
  <rect x="370" y="330" width="1005" height="420" rx="12" fill="#ECFDF5" stroke="#10B981" stroke-width="2" stroke-dasharray="6 4" />
  
  <!-- ASG Title Badge: Positioned cleanly in the center (X: 620 to 1120) with NO arrows cutting through -->
  <rect x="620" y="320" width="500" height="22" rx="4" fill="#059669" />
  <text x="870" y="335" font-family="'Segoe UI', Roboto, sans-serif" font-size="10.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">AUTO SCALING GROUP: hotstar-asg (Min: 1, Desired: 1, Max: 4)</text>

  <!-- SUBNET 1 (ap-south-1a | X: 385, W: 470) -->
  <g transform="translate(385, 350)">
    <rect width="470" height="385" rx="10" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1.5" />
    <rect x="14" y="12" width="220" height="22" rx="4" fill="#16A34A" />
    <text x="124" y="27" font-family="'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle">PUBLIC SUBNET 1 (ap-south-1a | 10.0.1.0/24)</text>

    <!-- Instance 1: Primary Baseline -->
    <g transform="translate(15, 48)" filter="url(#c-shadow-4)">
      <rect width="440" height="150" rx="8" fill="#FFFBEB" stroke="#F59E0B" stroke-width="1.5" />
      <rect x="12" y="12" width="115" height="20" rx="4" fill="#D97706" />
      <text x="69" y="26" font-family="'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">PRIMARY (ACTIVE)</text>
      <text x="135" y="28" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#B45309">EC2 Instance 1 (t3.micro)</text>
      <text x="12" y="58" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• AMI: Amazon Linux 2023 | 2 vCPUs, 1 GiB RAM</text>
      <text x="12" y="80" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Runtime: FastAPI + Uvicorn (4 worker processes on :80)</text>
      <text x="12" y="102" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Workload: /work CPU matrix burn + /health probe</text>
      <text x="12" y="124" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#D97706">• Baseline capacity (Runs 24/7 at minimum cost: $7.45/mo)</text>
    </g>

    <!-- Instance 2: Scale-Out Unit -->
    <g transform="translate(15, 215)" filter="url(#c-shadow-4)">
      <rect width="440" height="150" rx="8" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1.5" />
      <rect x="12" y="12" width="125" height="20" rx="4" fill="#059669" />
      <text x="74" y="26" font-family="'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">SCALE-OUT UNIT</text>
      <text x="145" y="28" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#065F46">EC2 Instance 2 (t3.micro)</text>
      <text x="12" y="58" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Launched automatically by CloudWatch High-CPU alarm</text>
      <text x="12" y="80" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• UserData bootstrap runs in 82 seconds from launch</text>
      <text x="12" y="102" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Passes ALB health checks and enters Target Group</text>
      <text x="12" y="124" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#059669">• Absorbs 50% of incoming load, relieving Instance 1</text>
    </g>
  </g>

  <!-- SUBNET 2 (ap-south-1b | X: 885, W: 470) -->
  <g transform="translate(885, 350)">
    <rect width="470" height="385" rx="10" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1.5" />
    <rect x="14" y="12" width="220" height="22" rx="4" fill="#16A34A" />
    <text x="124" y="27" font-family="'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="bold" fill="#FFFFFF" text-anchor="middle">PUBLIC SUBNET 2 (ap-south-1b | 10.0.2.0/24)</text>

    <!-- Instance 3: Scale-Out Multi-AZ Unit -->
    <g transform="translate(15, 48)" filter="url(#c-shadow-4)">
      <rect width="440" height="150" rx="8" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1.5" />
      <rect x="12" y="12" width="135" height="20" rx="4" fill="#059669" />
      <text x="79" y="26" font-family="'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">MULTI-AZ EXPANSION</text>
      <text x="155" y="28" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#065F46">EC2 Instance 3 (t3.micro)</text>
      <text x="12" y="58" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Multi-AZ rebalancing distributes across Availability Zones</text>
      <text x="12" y="80" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Protects against single AZ physical datacenter outages</text>
      <text x="12" y="102" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Same immutable launch template configuration</text>
      <text x="12" y="124" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#059669">• Handles third tier of Locust load spike</text>
    </g>

    <!-- Instance 4: Peak Burst Unit -->
    <g transform="translate(15, 215)" filter="url(#c-shadow-4)">
      <rect width="440" height="150" rx="8" fill="#FFFFFF" stroke="#86EFAC" stroke-width="1.5" />
      <rect x="12" y="12" width="135" height="20" rx="4" fill="#059669" />
      <text x="79" y="26" font-family="'Segoe UI', Roboto, sans-serif" font-size="9" font-weight="bold" fill="#FFFFFF" text-anchor="middle">MAX PEAK CEILING</text>
      <text x="155" y="28" font-family="'Segoe UI', Roboto, sans-serif" font-size="14.5" font-weight="bold" fill="#065F46">EC2 Instance 4 (t3.micro)</text>
      <text x="12" y="58" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Reaches Max Capacity = 4 instances under 250 users</text>
      <text x="12" y="80" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• Total fleet capacity reaches 8 vCPUs and 4 GiB RAM</text>
      <text x="12" y="102" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" fill="#334155">• System latency stabilizes at 46ms median</text>
      <text x="12" y="124" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#059669">• Gracefully scaled in after load test completion</text>
    </g>
  </g>

  <!-- CLEAN ORTHOGONAL CONNECTORS IN OPEN CORRIDOR (Y: 275 to 330) -->
  <!-- ALB to Subnet 1: Straight down at X: 480 (completely misses the ASG badge at X: 620-1120) -->
  <path d="M 480 275 L 480 350" fill="none" stroke="#0284C7" stroke-width="3" marker-end="url(#arr-blue-4)" />

  <!-- ALB to Subnet 2: Exits ALB at (640, 275), drops to Y=298 in open corridor, runs across to X=1180, drops to Subnet 2 -->
  <path d="M 640 275 L 640 298 L 1180 298 L 1180 350" fill="none" stroke="#0284C7" stroke-width="3" marker-end="url(#arr-blue-4)" />

  <!-- CloudWatch Scale Trigger: Exits CloudWatch at far right (X: 1300, Y: 275), drops down into ASG at (1300, 330) -->
  <path d="M 1300 275 L 1300 330" fill="none" stroke="#DC2626" stroke-width="3.5" marker-end="url(#arr-red-4)" />
  <rect x="1225" y="287" width="145" height="22" rx="4" fill="#DC2626" />
  <text x="1297" y="302" font-family="'Segoe UI', Roboto, sans-serif" font-size="8.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">ASG Scale Trigger</text>

  <!-- BOTTOM CALLOUT BANNER (Y: 790 to 875) -->
  <g transform="translate(45, 790)" filter="url(#c-shadow-4)">
    <rect width="1350" height="85" rx="10" fill="#ECFDF5" stroke="#059669" stroke-width="2" />
    <rect x="18" y="18" width="135" height="50" rx="6" fill="#059669" />
    <text x="85" y="38" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">AUTONOMOUS</text>
    <text x="85" y="55" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="bold" fill="#FFFFFF" text-anchor="middle">SCALING</text>
    <text x="175" y="38" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#065F46">• Proactive 50% CPU Threshold: Prevents queue starvation and CPU thrashing before 100% saturation, providing safety cushion for 82s EC2 boot.</text>
    <text x="175" y="60" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="bold" fill="#065F46">• Dual-AZ High Availability: Automatic cross-zone balancing guarantees resilience against single datacenter failures while maintaining 46ms median response time.</text>
  </g>
</svg>"""
    render_svg(svg, "poc_aws_architecture.png")


def main():
    print("Generating all 4 vector SVG diagrams...")
    generate_diagram_1()
    generate_diagram_2()
    generate_diagram_3()
    generate_diagram_4()
    print("All 4 diagrams generated successfully!")

if __name__ == "__main__":
    main()
