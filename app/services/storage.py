from supabase import create_client
from app.config import settings
import uuid

supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


def upload_image_to_supabase(upload_file):
    """
    Upload FastAPI UploadFile to Supabase Storage
    Returns public URL
    """

    # ✅ Unique filename
    file_name = f"{uuid.uuid4()}-{upload_file.filename}"

    # ✅ Read bytes from UploadFile
    file_bytes = upload_file.file.read()

    # ✅ Upload bytes
    supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
        file_name,
        file_bytes,
        {"content-type": upload_file.content_type},
    )

    # ✅ Get Public URL
    public_url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(file_name)

    return public_url
