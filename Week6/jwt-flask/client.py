import requests


url = "http://localhost:5000/api/login"
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json={"username": "admin", "password": "password"})
token = response.json()["accessToken"]

print(token)

url = "http://localhost:5000/api/protected"
headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.get(url, headers=headers)
fail_response = requests.get(url)


print(response.json())
print(fail_response.json())