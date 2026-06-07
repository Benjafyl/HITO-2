"""
SkyConnect Airlines - Locust load test.

Web mode:
  locust -f locustfile.py --host=http://backend:8000

Headless CSV export:
  locust -f locustfile.py \
    --host=http://backend:8000 \
    --users 1000 \
    --spawn-rate 50 \
    --run-time 5m \
    --headless \
    --csv=results/before

Generated files:
  results/before_stats.csv
  results/before_stats_history.csv
  results/before_failures.csv
"""

from locust import HttpUser, between, task


class SkyConnectUser(HttpUser):
    """
    Simulates Cyber Day traffic.

    Task distribution:
      - GET /flights: 70% of requests, critical endpoint.
      - GET /routes: 20% of requests.
      - GET /aircraft: 10% of requests.
    """

    wait_time = between(1, 3)

    @task(7)
    def search_flights(self):
        with self.client.get("/flights", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Unexpected status {response.status_code}")

    @task(2)
    def get_routes(self):
        self.client.get("/routes")

    @task(1)
    def get_aircraft(self):
        self.client.get("/aircraft")
