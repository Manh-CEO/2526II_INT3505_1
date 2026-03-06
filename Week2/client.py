import requests




response = requests.get('http://localhost:5000')
print(response.text)

response = requests.get('http://localhost:5000/books')
print(f"get all books: {response.json()}")
