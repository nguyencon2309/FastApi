import cloudinary.uploader


def upload_image(file):
    result = cloudinary.uploader.upload(file)
    return {
        "url": result["secure_url"],
        "public_id": result["public_id"]
    }


def delete_image(public_id: str):
    result = cloudinary.uploader.destroy(public_id)
    return result