source .venv/bin/activate
  
# 2. Check live ALB is healthy
curl -s http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com/health | jq .
  
# 3. Test CPU endpoint
curl -s "http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com/work?n=300000" | jq .
  
# 4. Live 3-Minute Auto-Scaling Demo
locust -f loadtest/locustfile.py --headless -u 60 -r 10 --run-time 3m --host http://hotstar-alb-2011340704.ap-south-1.elb.amazonaws.com