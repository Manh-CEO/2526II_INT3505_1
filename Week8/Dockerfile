# Dockerfile cho Week 8 - Newman Test Suite
FROM postman/newman:latest

# Cài đặt thêm các reporter cần thiết
RUN npm install -g newman-reporter-htmlextra newman-reporter-openapi

# Thiết lập thư mục làm việc
WORKDIR /etc/newman

# Copy toàn bộ thư mục hiện tại vào container (optional, hoặc dùng volume mount)
# COPY . .

# Lệnh mặc định khi chạy container
ENTRYPOINT ["newman"]
