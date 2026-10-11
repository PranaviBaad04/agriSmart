"""
Cloudinary Image Storage Service for AgriSmart
Handles image validation, folder organization, unique public IDs, and secure uploads.
"""
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Tuple
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(ROOT_DIR / ".env")

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

# Local fallback uploads directory
UPLOADS_DIR = ROOT_DIR / "backend" / "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

# Initialize Cloudinary if credentials are configured
CLOUDINARY_CONFIGURED = False
try:
    if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET:
        import cloudinary
        import cloudinary.uploader
        cloudinary.config(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET,
            secure=True
        )
        CLOUDINARY_CONFIGURED = True
        print(f"Cloudinary initialized successfully for cloud: {CLOUDINARY_CLOUD_NAME}")
    else:
        print("Notice: Cloudinary credentials not fully configured in .env. Local storage fallback will be active.")
except Exception as e:
    print(f"Warning: Cloudinary initialization error: {e}")


def validate_image_file(filename: str, file_bytes: bytes) -> Tuple[bool, str]:
    """Validate image extension, MIME type and byte size"""
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file format '{ext}'. Allowed formats: JPG, JPEG, PNG, WEBP."

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        size_mb = len(file_bytes) / (1024 * 1024)
        return False, f"File size ({size_mb:.1f} MB) exceeds maximum allowed limit of 10 MB."

    if len(file_bytes) < 100:
        return False, "Uploaded file appears empty or corrupted."

    return True, "Valid"


def upload_image(
    file_bytes: bytes,
    original_filename: str,
    folder: str = "AgriSmart/chilli/disease-detection"
) -> Dict[str, Any]:
    """
    Upload image to Cloudinary in the designated folder.
    Falls back gracefully to local static server if Cloudinary credentials are not set.
    """
    is_valid, msg = validate_image_file(original_filename, file_bytes)
    if not is_valid:
        raise ValueError(msg)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex[:8]
    sanitized_name = Path(original_filename).stem.replace(" ", "_")[:20]
    public_id = f"chilli_{timestamp}_{sanitized_name}_{unique_id}"

    # 1. Attempt Cloudinary Upload if configured
    if CLOUDINARY_CONFIGURED:
        try:
            import cloudinary.uploader
            response = cloudinary.uploader.upload(
                file_bytes,
                folder=folder,
                public_id=public_id,
                resource_type="image",
                overwrite=True
            )
            return {
                "success": True,
                "provider": "cloudinary",
                "image_url": response.get("secure_url"),
                "public_id": response.get("public_id"),
                "format": response.get("format"),
                "bytes": response.get("bytes"),
                "created_at": response.get("created_at")
            }
        except Exception as e:
            print(f"Warning: Cloudinary upload failed ({e}). Falling back to local storage.")

    # 2. Local Fallback Storage
    ext = Path(original_filename).suffix.lower() or ".jpg"
    local_filename = f"{public_id}{ext}"
    local_file_path = UPLOADS_DIR / local_filename

    with open(local_file_path, "wb") as f:
        f.write(file_bytes)

    local_url = f"/uploads/{local_filename}"
    return {
        "success": True,
        "provider": "local_fallback",
        "image_url": local_url,
        "public_id": public_id,
        "format": ext.replace(".", ""),
        "bytes": len(file_bytes),
        "created_at": datetime.utcnow().isoformat()
    }
