from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from bson import ObjectId
from app.utils.security import verify_token
from app.core.database import db
user_collection = db["user"]



async def check_token_middleware(request: Request) -> dict:
    """
    Middleware check token: Tự động lấy token từ Header Authorization,
    xác thực và trả về thông tin User hiện tại (Không dùng OAuth2).
    """
    # 1. Lấy chuỗi Authorization từ Header của request
    auth_header = request.headers.get("Authorization")
    
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Thiếu Header Authorization! Vui lòng đăng nhập."
        )
    
    # 2. Tách chữ 'Bearer ' ra khỏi token (nếu phía Client gửi dạng: Bearer <token>)
    try:
        if auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            token = auth_header # Trường hợp client chỉ gửi mỗi chuỗi token thô
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Định dạng Token không hợp lệ (Phải là 'Bearer <token>')."
        )

    # 3. Giải mã và kiểm tra tính hợp lệ của Token
    user_id = verify_token(token)
    if user_id is None:
        # 🛡️ Chặn đứng nếu token hết hạn hoặc giả mạo
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã hết hạn!"
        )
        
    # 4. Tìm kiếm người dùng trong Database
    try:
        user = user_collection.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User ID trong token không đúng định dạng ObjectId!"
        )
        
    if user is None:
        # 🛡️ Chặn đứng nếu tài khoản đã bị xóa khỏi DB
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại trên hệ thống!"
        )
        
    # Nếu tất cả đều hợp lệ, trả về thông tin user
    return user

def check_admin_middleware(current_user: dict = Depends(check_token_middleware)) -> dict:
    """Middleware check admin: Kế thừa từ check_token, chặn nếu không phải admin"""
    
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Bạn không có quyền truy cập! Chức năng này chỉ dành cho Admin."
        )
    return current_user