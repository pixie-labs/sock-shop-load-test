import base64

from locust import HttpUser, TaskSet, task
from random import randint, choice


class WebTasks(TaskSet):

    @task
    def load(self):
        base64string = base64.encodebytes(b'user:password').replace(b'\n', b'').decode()

        catalogue = self.client.get("/catalogue").json()
        # This sometimes fails under load.
        if "error" in catalogue:
            return
        category_item = choice(catalogue)
        item_id = category_item["id"]

        self.client.get("/")
        self.client.get("/login", headers={"Authorization":"Basic %s" % base64string})
        self.client.get("/category.html")
        self.client.get("/catalogue?tags=brown,geek")
        self.client.get("/detail.html?id={}".format(item_id))
        self.client.delete("/cart")
        self.client.post("/cart", json={"id": item_id, "quantity": 1})
        self.client.get("/basket.html")
        self.client.post("/orders")


class Web(HttpUser):
    tasks = [WebTasks]
    min_wait = 0
    max_wait = 0
