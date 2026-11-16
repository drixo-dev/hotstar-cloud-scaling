from locust import HttpUser, LoadTestShape, task, between


class WebUser(HttpUser):
    """
    Simulates a streaming viewer requesting match data.
    Hits the CPU-intensive /work endpoint to generate server load.
    """
    wait_time = between(0.1, 0.4)

    @task
    def work(self):
        # n=300000 consumes ~30-50ms CPU per request, quickly elevating instance CPU
        self.client.get("/work?n=300000", name="/work")

    @task(1)
    def health_check(self):
        # Occasional health check call
        self.client.get("/health", name="/health")


# Only register SpikeShape if explicitly requested via USE_SHAPE=1
# This allows standard CLI flags (-u, -r, --run-time) to control fast live demos cleanly without warnings
import os

if os.environ.get("USE_SHAPE", "0") == "1":
    class SpikeShape(LoadTestShape):
        """
        Spike load profile replicating Hotstar live cricket traffic:
        1. Warm-up (0-120s): 20 users (steady baseline)
        2. Tsunami Spike (120-180s): Rapid ramp to 150 users (match start / wicket)
        3. Plateau (180-600s): 150 users for 7 minutes (triggers CPU > 50% scale-out)
        4. Post-match Drop (600-720s): Drop to 20 users (triggers scale-in cool-down)
        5. Tail (720-780s): 20 users settling down
        """
        stages = [
            # (end_time_seconds, target_users, spawn_rate_per_second)
            (120, 20, 5),      # Stage 1: Warm-up baseline
            (180, 150, 25),    # Stage 2: Spike jump to heavy load
            (600, 150, 25),    # Stage 3: Plateau - holds load while ASG scales out
            (720, 20, 25),     # Stage 4: Drop - traffic subsides
            (780, 20, 5),      # Stage 5: Tail - baseline recovery
        ]

        def tick(self):
            run_time = self.get_run_time()
            for end, users, rate in self.stages:
                if run_time < end:
                    return users, rate
            return None

