"""
AWS S3 Storage Integration for Production File Uploads
Replace local file storage with cloud storage for scalability
"""
import boto3
from botocore.exceptions import ClientError
import os
from werkzeug.utils import secure_filename
import uuid

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    region_name=os.environ.get('AWS_S3_REGION_NAME', 'ap-southeast-1')
)

BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', 'sportsbuilder-uploads')
USE_S3 = os.environ.get('USE_S3_STORAGE', 'false').lower() == 'true'

def upload_file_to_s3(file, folder='uploads'):
    """
    Upload file to S3 and return public URL
    
    Args:
        file: FileStorage object from Flask request
        folder: S3 folder/prefix (default: 'uploads')
    
    Returns:
        str: Public URL of uploaded file or None if failed
    """
    if not file or not file.filename:
        return None
    
    # Generate unique filename
    filename = secure_filename(file.filename)
    base, ext = os.path.splitext(filename)
    unique_filename = f"{base}_{uuid.uuid4().hex[:8]}{ext}"
    s3_key = f"{folder}/{unique_filename}"
    
    try:
        # Upload to S3
        s3_client.upload_fileobj(
            file,
            BUCKET_NAME,
            s3_key,
            ExtraArgs={
                'ContentType': file.content_type or 'application/octet-stream',
                'ACL': 'public-read',
                'CacheControl': 'max-age=31536000',  # Cache for 1 year
            }
        )
        
        # Return public URL
        region = os.environ.get('AWS_S3_REGION_NAME', 'ap-southeast-1')
        url = f"https://{BUCKET_NAME}.s3.{region}.amazonaws.com/{s3_key}"
        
        print(f"✅ Uploaded to S3: {url}")
        return url
        
    except ClientError as e:
        print(f"❌ Error uploading to S3: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None


def delete_file_from_s3(file_url):
    """
    Delete file from S3 given its URL
    
    Args:
        file_url: Full S3 URL of the file
    
    Returns:
        bool: True if deleted successfully, False otherwise
    """
    if not file_url or BUCKET_NAME not in file_url:
        return False
    
    try:
        # Extract S3 key from URL
        # URL format: https://bucket.s3.region.amazonaws.com/folder/file.jpg
        parts = file_url.split('.amazonaws.com/')
        if len(parts) < 2:
            return False
        
        s3_key = parts[1]
        
        # Delete from S3
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=s3_key)
        print(f"✅ Deleted from S3: {s3_key}")
        return True
        
    except ClientError as e:
        print(f"❌ Error deleting from S3: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def list_bucket_files(prefix='uploads/', max_keys=1000):
    """
    List files in S3 bucket (useful for debugging/admin)
    
    Args:
        prefix: Folder prefix to filter
        max_keys: Maximum number of files to return
    
    Returns:
        list: List of file keys
    """
    try:
        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=prefix,
            MaxKeys=max_keys
        )
        
        if 'Contents' not in response:
            return []
        
        files = [obj['Key'] for obj in response['Contents']]
        return files
        
    except ClientError as e:
        print(f"❌ Error listing S3 files: {e}")
        return []


def get_file_size(file_url):
    """
    Get file size from S3
    
    Args:
        file_url: Full S3 URL of the file
    
    Returns:
        int: File size in bytes or None if failed
    """
    if not file_url or BUCKET_NAME not in file_url:
        return None
    
    try:
        parts = file_url.split('.amazonaws.com/')
        if len(parts) < 2:
            return None
        
        s3_key = parts[1]
        
        response = s3_client.head_object(Bucket=BUCKET_NAME, Key=s3_key)
        return response['ContentLength']
        
    except ClientError as e:
        print(f"❌ Error getting file size: {e}")
        return None


def generate_presigned_url(file_url, expiration=3600):
    """
    Generate a presigned URL for temporary private access
    Useful for private files that need temporary public access
    
    Args:
        file_url: Full S3 URL of the file
        expiration: URL expiration time in seconds (default: 1 hour)
    
    Returns:
        str: Presigned URL or None if failed
    """
    if not file_url or BUCKET_NAME not in file_url:
        return None
    
    try:
        parts = file_url.split('.amazonaws.com/')
        if len(parts) < 2:
            return None
        
        s3_key = parts[1]
        
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': s3_key},
            ExpiresIn=expiration
        )
        
        return presigned_url
        
    except ClientError as e:
        print(f"❌ Error generating presigned URL: {e}")
        return None


# Fallback to local storage if S3 is not configured
def save_upload_local(file, upload_folder='static/uploads'):
    """
    Fallback: Save file locally (for development)
    
    Args:
        file: FileStorage object from Flask request
        upload_folder: Local folder path
    
    Returns:
        str: Relative path to uploaded file
    """
    if not file or not file.filename:
        return None
    
    filename = secure_filename(file.filename)
    base, ext = os.path.splitext(filename)
    unique_filename = f"{base}_{uuid.uuid4().hex[:8]}{ext}"
    
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, unique_filename)
    file.save(filepath)
    
    # Return relative path for use in templates
    return f"uploads/{unique_filename}"


def delete_upload_local(rel_path, static_folder='static'):
    """
    Fallback: Delete local file
    
    Args:
        rel_path: Relative path like 'uploads/file.jpg'
        static_folder: Static folder path
    
    Returns:
        bool: True if deleted successfully
    """
    if not rel_path or not isinstance(rel_path, str):
        return False
    
    abs_path = os.path.join(static_folder, rel_path)
    
    try:
        if os.path.exists(abs_path):
            os.remove(abs_path)
            return True
    except OSError as e:
        print(f"❌ Error deleting local file: {e}")
    
    return False


# Main functions that choose between S3 and local storage
def save_upload(file):
    """
    Save uploaded file to S3 (production) or local storage (development)
    
    Args:
        file: FileStorage object from Flask request
    
    Returns:
        str: URL (S3) or relative path (local) of uploaded file
    """
    if USE_S3:
        return upload_file_to_s3(file)
    else:
        return save_upload_local(file)


def delete_upload(file_path):
    """
    Delete uploaded file from S3 (production) or local storage (development)
    
    Args:
        file_path: URL (S3) or relative path (local) of file
    
    Returns:
        bool: True if deleted successfully
    """
    if USE_S3 and file_path and 's3' in file_path:
        return delete_file_from_s3(file_path)
    else:
        return delete_upload_local(file_path)


# Test function
if __name__ == "__main__":
    print("🧪 Testing S3 Storage Configuration")
    print(f"Bucket: {BUCKET_NAME}")
    print(f"Region: {os.environ.get('AWS_S3_REGION_NAME', 'ap-southeast-1')}")
    print(f"Use S3: {USE_S3}")
    
    # Test listing files
    print("\n📁 Files in bucket:")
    files = list_bucket_files()
    for f in files[:10]:  # Show first 10
        print(f"  - {f}")
    
    print(f"\n✅ Total files: {len(files)}")
