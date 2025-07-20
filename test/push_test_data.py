import requests
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"  

# Test users list
users = [
    {
        "id": "user1",
        "firstName": "Long",
        "lastName": "Hoang",
        "phoneNumber": "0123456789",
        "email": "long@example.com",
        "avatar": None,
        "gender": "male",
        "jobTitle": "Developer",
        "company": "ABC Corp",
        "city": "Hanoi",
        "state": "HN"
    },
    {
        "id": "user2",
        "firstName": "Anh",
        "lastName": "Nguyen",
        "phoneNumber": "0987654321",
        "email": "anh@example.com",
        "avatar": None,
        "gender": "female",
        "jobTitle": "Designer",
        "company": "XYZ Ltd",
        "city": "HCM",
        "state": "SG"
    },
    {
        "id": "user3",
        "firstName": "John",
        "lastName": "Doe",
        "phoneNumber": "0911222333",
        "email": "john.doe@example.com",
        "avatar": None,
        "gender": "male",
        "jobTitle": "Product Manager",
        "company": "Tech Innovators",
        "city": "Hanoi",
        "state": "HN"
    },
    {
        "id": "user4",
        "firstName": "Anna",
        "lastName": "Tran",
        "phoneNumber": "0933444555",
        "email": "anna.tran@example.com",
        "avatar": None,
        "gender": "female",
        "jobTitle": "Marketing Specialist",
        "company": "Creative Minds",
        "city": "HCM",
        "state": "SG"
    }
]

# Test events list
events = [
    {
        "id": "event1",
        "slug": "event-1",
        "title": "Event 1",
        "description": "This is test event number 1",
        "startAt": (datetime.now() + timedelta(days=1)).isoformat(),
        "endAt": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
        "venue": "Hall A",
        "maxCapacity": 100,
        "owner": "user1",
        "hosts": ["user1", "user2", "user3", "user4"]
    },
    {
        "id": "event2",
        "slug": "event-2",
        "title": "Event 2",
        "description": "This is test event number 2",
        "startAt": (datetime.now() + timedelta(days=2)).isoformat(),
        "endAt": (datetime.now() + timedelta(days=2, hours=3)).isoformat(),
        "venue": "Hall B",
        "maxCapacity": 50,
        "owner": "user2",
        "hosts": ["user2", "user3", "user4"]
    }
]

def push_users():
    for user in users:
        res = requests.post(f"{BASE_URL}/users/create-user", json=user)
        print(f"Create user {user['id']}: {res.status_code} - {res.json()}")

def push_events():
    for event in events:
        res = requests.post(f"{BASE_URL}/events/create-event", json=event)
        print(f"Create event {event['id']}: {res.status_code} - {res.json()}")

if __name__ == "__main__":
    push_users()
    push_events()