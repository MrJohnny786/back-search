import json
import unittest
from app import app


class TestAPI(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_search_data(self):
        response = self.app.post("/api/data/search", json={"name": "shirt"})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("data" in data)
        self.assertTrue("total_count" in data)
        self.assertTrue("total_pages" in data)
        self.assertTrue("current_page" in data)
        self.assertTrue("limit" in data)

    def test_search_data_no_name(self):
        response = self.app.post("/api/data/search", json={})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertTrue("error" in data)

    def test_search_data_not_found(self):
        response = self.app.post(
            "/api/data/search", json={"name": "qwegfewqrgwerghwer"}
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertTrue("error" in data)

    def test_search_data_invalid_page(self):
        response = self.app.post(
            "/api/data/search", json={"name": "shirt", "page": "invalid"}
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("data" in data)

    def test_search_data_invalid_limit(self):
        response = self.app.post(
            "/api/data/search", json={"name": "shirt", "limit": "invalid"}
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("data" in data)

    def test_search_data_negative_page(self):
        response = self.app.post("/api/data/search", json={"name": "shirt", "page": -1})
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue("data" in data)


if __name__ == "__main__":
    unittest.main()
# flake8: noqa
