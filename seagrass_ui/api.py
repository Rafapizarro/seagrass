import requests
import os


class APIRequest:
    def __init__(self):
        host = os.environ.get("API_HOST")
        port = os.environ.get("API_PORT")
        self.url = f"{host}:{port}/"

    def get(self, endpoint, query=None):
        if query:
            endpoint += "?"
            i = 0
            for q, val in query.items():
                if i != 0:
                    endpoint += "&"
                else:
                    i += 1
                endpoint += f"{q}={'+'.join(map(str, val))}"
        response = requests.get(self.url + endpoint)
        os.write(1, f"endpoint: {self.url + endpoint}\n".encode())

        return response.json()
