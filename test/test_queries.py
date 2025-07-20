import requests
import json

BASE_URL = "http://localhost:8000"  

def pretty_print(title, data):
    print("=" * 60)
    print(f"{title}")
    print("=" * 60)
    print(json.dumps(data, indent=4, ensure_ascii=False))
    print("\n")

def test_query():
    queries = [
        {
            "company": "ABC Corp",
            "pagination": True,
            "limit": 10
        },
        {
            "city": "Hanoi",
            "state": "HN",
            "pagination": True,
            "limit": 1,
            "ascending": False
        }
    ]
    res = requests.post(f"{BASE_URL}/users/get-users", json=queries)
    pretty_print("Query by company result:", res.json())


if __name__ == "__main__":
    test_query()