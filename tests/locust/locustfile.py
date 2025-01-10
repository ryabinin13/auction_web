from datetime import datetime
import random
from locust import HttpUser, between, task

class SimpleUser(HttpUser):
    wait_time = between(1, 3)

    # @task
    # def registration_test(self):
    #     registration_data = {
    #             "username": f"test_user_{random.randint(1, 10)}",
    #             "email": f"test_{random.randint(1, 10)}@example.com",
    #             "birthday": "2000-01-01",
    #             "sex": "male",
    #             "phone_number": "123-456-7890",
    #             "password1": "test_password123",
    #             "password2": "test_password123"
    #        }
    #     self.client.post("/registration", json=registration_data)

    # @task
    # def login_test(self):
    #     login_data = {
    #         "email": f"test_{random.randint(1, 10)}@example.com",
    #         "password": "test_password123"
    #     }
    #     self.client.post("/login", json=login_data)


    @task
    def start_auction_test(self):
        product_data = {
            "name": "test",
            "discription": "test",
            "start_price": 0,
            "end_date": datetime.now() + datetime.timedelta(minutes=random.randint(10, 20))
            }
        self.client.post("/start_auction", json=product_data)
