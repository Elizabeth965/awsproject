import boto3
import os

# Configuration
BUCKET_NAME = 'secure-backup-system'  # Replace with your bucket name

# Initialize S3 client
s3 = boto3.client('s3')

def upload_file(file_path):
    """Uploads a file to the specified S3 bucket."""
    try:
        file_name = os.path.basename(file_path)
        s3.upload_file(
            file_path, BUCKET_NAME, file_name,
            ExtraArgs={'ServerSideEncryption': 'AES256'}  # Ensures encryption
        )
        print(f"{file_name} uploaded successfully to {BUCKET_NAME}")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")

# Test the function
if __name__ == "__main__":
    # Replace with the file path you want to upload
    test_file = '/Users/ms.elizabethlisamondol/Desktop/test_upload.txt'
    upload_file(test_file)
