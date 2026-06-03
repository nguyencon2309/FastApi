import bcrypt
from datetime import datetime, timedelta
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

def get_password_hash(password: str) -> str:
    """Mã hóa mật khẩu thô thành chuỗi hash để lưu vào DB"""
    # Thư viện bcrypt yêu cầu dữ liệu đầu vào phải ở dạng bytes
    password_bytes = password.encode('utf-8')
    
    # Tạo chuỗi muối (salt) và băm mật khẩu
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # Chuyển ngược từ bytes về string để lưu vào MongoDB dễ dàng
    return hashed_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Đối chiếu mật khẩu thô Client gửi lên với mật khẩu đã mã hóa trong DB"""
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    
    # Hàm checkpw tự động so sánh an toàn
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

def create_access_token(data: dict) -> str:
    """Hàm tạo token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

def verify_token(token: str) -> str | None:
    """Hàm xác thực token sơ cấp, bóc tách và trả về user_id"""
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        user_id: str = payload.get("sub")
        return user_id
    except jwt.PyJWTError:
        return None