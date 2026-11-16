source .venv/bin/activate
  
# 2. Automated Smoke Test (Verifies /, /health, and /work in 2 seconds)
python loadtest/local_smoke_test.py http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com

# 3. Check live ALB health check directly
curl -s http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com/health | jq .
  
# 3. Test CPU endpoint
curl -s "http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com/work?n=300000" | jq .
  
# 4. Live 3-Minute Auto-Scaling Demo
locust -f loadtest/locustfile.py --headless -u 60 -r 10 --run-time 3m --host http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com