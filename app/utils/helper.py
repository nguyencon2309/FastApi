def pydantic_mongo_helper(document: dict) -> dict:
    """
    Hàm helper chuyển đổi tài liệu thô từ MongoDB thành dạng Pydantic hiểu được.
    Biến đổi '_id' (ObjectId) thành 'id' (String) và xóa '_id' gốc đi.
    """
    if not document:
        return document
        
    # Ép kiểu ObjectId sang chuỗi và gán vào key 'id'
    if "_id" in document:
        document["id"] = str(document["_id"])
        del document["_id"] # Xóa _id cũ đi cho sạch dữ liệu
        
    return document