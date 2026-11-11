from locust import HttpUser, task, between

class WebsitePerformanceUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def load_home_page(self):
        self.client.get("/")

    @task(1)
    def load_login_page(self):
        self.client.get("/login")