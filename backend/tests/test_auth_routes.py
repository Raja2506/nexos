import requests

BASE_URL = "http://localhost:8000"

def test_signup_and_login():
    signup_payload = {
        "email": "testuser@example.com",
        "password": "TestPass123",
        "name": "Test User",
    }

    r = requests.post(f"{BASE_URL}/auth/signup", json=signup_payload)
    print("Signup status:", r.status_code)
    print("Signup response:", r.json())

    login_payload = {
        "email": "testuser@example.com",
        "password": "TestPass123",
    }
    r2 = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
    print("\nLogin status:", r2.status_code)
    print("Login response:", r2.json())

    wrong_payload = {
        "email": "testuser@example.com",
        "password": "WrongPassword",
    }
    r3 = requests.post(f"{BASE_URL}/auth/login", json=wrong_payload)
    print("\nWrong password status (should be 401):", r3.status_code)


if __name__ == "__main__":
    test_signup_and_login()
