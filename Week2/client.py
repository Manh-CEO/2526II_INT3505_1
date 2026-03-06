import requests

BASE_URL = 'http://localhost:5000'

response = requests.get(f'{BASE_URL}/')
print(f"Server status: {response.text}")

login_data = {'username': 'admin', 'password': '123'}
login_response = requests.post(f'{BASE_URL}/login', json=login_data)

if login_response.status_code == 200:
    token = login_response.json().get('token')
    print(f"Lấy Token thành công: {token[:20]}...")
    
    headers = {'Authorization': token}
    
    book_response = requests.get(f'{BASE_URL}/books', headers=headers)
    
    if book_response.status_code == 200:
        print(f"Danh sách sách: {book_response.json()}")
    else:
        print(f"Lỗi lấy sách: {book_response.status_code}")
else:
    print("Đăng nhập thất bại!")

bad_response = requests.get(f'{BASE_URL}/books')
print(f"Kết quả (mong đợi lỗi 401): {bad_response.status_code} - {bad_response.json()}")