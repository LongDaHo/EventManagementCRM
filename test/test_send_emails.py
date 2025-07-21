import requests

BASE_URL = "http://localhost:8000"


def test_send_email():
    queries = [
        {
            "company": "ABC Corp",
            "subject": "Test email",
            "body": "This is a test email",
        },
        {
            "city": "Hanoi",
            "state": "HN",
            "subject": "Test email",
            "body": "This is a test email",
        },
    ]
    res = requests.post(f"{BASE_URL}/email/send-email", json=queries)
    print("Send email result:", res.json())


if __name__ == "__main__":
    test_send_email()
