import requests
import time

BASE_URL = 'http://localhost:5000'

browser_cache = {
    "etag": None,
    "data": None
}
login_res = requests.post(f'{BASE_URL}/login', json={'username': 'admin', 'password': '123'})
token = login_res.json().get('token')
headers = {'Authorization': token}

def get_books_with_cache():
    global browser_cache
    
    if browser_cache["etag"]:
        headers['If-None-Match'] = browser_cache["etag"]
    
    response = requests.get(f'{BASE_URL}/books', headers=headers)
    
    if response.status_code == 200:
        print("-> [200 OK] Dữ liệu mới hoặc đã thay đổi. Đang lưu vào Cache...")
        browser_cache["data"] = response.json()
        browser_cache["etag"] = response.headers.get('ETag')
        return browser_cache["data"]
        
    elif response.status_code == 304:
        print("-> [304 Not Modified] Server nói dữ liệu vẫn thế.")
        print("-> Đang lấy dữ liệu từ 'Kho lưu trữ' (browser_cache['data']) để hiển thị...")
        return browser_cache["data"]

print("\n--- Gọi lần 1 ---")
books = get_books_with_cache()
print(f"Hiển thị: {books}")

print("\n--- Gọi lần 2 (Cache đang hoạt động) ---")
time.sleep(2)
books = get_books_with_cache()
print(f"Hiển thị từ Cache: {books}")