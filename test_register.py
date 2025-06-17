import requests
import json
import time
import sys

def test_registration():
    url = "http://127.0.0.1:8000/register/"
    
    data = {
        "username": "testuser5",
        "password": "testpass123",
        "email": "test5@example.com",
        "first_name": "Test",
        "last_name": "User",
        "role": "user"
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("Testing registration endpoint...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    # Give the server a moment to start
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        print("\n=== Response ===")
        print(f"Status Code: {response.status_code}")
        print("Headers:", json.dumps(dict(response.headers), indent=2))
        print("Body:", response.text)
        
        if response.status_code == 201:
            print("\n✅ Registration successful!")
        else:
            print("\n❌ Registration failed.")
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Request failed: {str(e)}")
        print("Make sure the Django development server is running.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    test_registration()
