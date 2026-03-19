import hmac
import hashlib
import base64
import json


def base64url_encode(data):
    if isinstance(data, dict):
        data = json.dumps(data).encode("utf-8")
    elif isinstance(data, str):
        data = data.encode("utf-8")
    encoded = base64.urlsafe_b64encode(data).decode("utf-8")
    return encoded.rstrip("=")


def create_jwt(payload, secret):
    header = {"alg": "HS256", "typ": "JWT"}

    encoded_header = base64url_encode(header)
    encoded_payload = base64url_encode(payload)

    signature_base = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    signature = hmac.new(
        secret.encode("utf-8"), signature_base, digestmod=hashlib.sha256
    ).digest()

    encoded_signature = base64.urlsafe_b64encode(signature).decode("utf-8").rstrip("=")

    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


SECRET_KEY = "my_super_secret_key"
data = {"user_id": 123, "name": "Manh", "admin": True}

token = create_jwt(data, SECRET_KEY)
print(f"Generated JWT:\n{token}")


def base64url_decode(payload):
    rem = len(payload) % 4
    if rem > 0:
        payload += "=" * (4 - rem)

    # Giải mã từ Base64URL sang Bytes, sau đó sang String
    decoded_bytes = base64.urlsafe_b64decode(payload)
    return json.loads(decoded_bytes.decode("utf-8"))


def decode_jwt(token):
    # Chia token thành 3 phần bằng dấu chấm
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Token không đúng định dạng JWT (phải có 3 phần)")

    header = base64url_decode(parts[0])
    payload = base64url_decode(parts[1])

    return header, payload


header, payload = decode_jwt(token)

print("--- HEADER ---")
print(json.dumps(header, indent=4))

print("\n--- PAYLOAD ---")
print(json.dumps(payload, indent=4))
