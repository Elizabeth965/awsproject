import boto3
import os
import time

# Configuration
BUCKET_NAME = 'secure-backup-system'  # Replace with your bucket name
FOLDER_PATH = '/Users/ms.elizabethlisamondol/Desktop/my picture aws'  # Replace with your folder path
CHECK_INTERVAL = 10  # Time (in seconds) to wait before checking the folder again

# Initialize S3 client
s3 = boto3.client('s3')

# Keep track of uploaded files
uploaded_files = set()

def upload_file(file_path):
    """Uploads a single file to S3."""
    try:
        file_name = os.path.basename(file_path)
        s3.upload_file(
            file_path, BUCKET_NAME, file_name,
            ExtraArgs={'ServerSideEncryption': 'AES256'}  # Ensures encryption
        )
        print(f"{file_name} uploaded successfully to {BUCKET_NAME}")
        return True
    except Exception as e:
        print(f"Error uploading file {file_name}: {str(e)}")
        return False

def monitor_and_upload(folder_path):
    """Continuously monitors a folder and uploads new files to S3."""
    while True:
        try:
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path) and file_name not in uploaded_files:
                    if upload_file(file_path):  # Upload the file
                        uploaded_files.add(file_name)  # Mark as uploaded
            print(f"Waiting for {CHECK_INTERVAL} seconds before checking again...")
            time.sleep(CHECK_INTERVAL)  # Wait before checking again
        except KeyboardInterrupt:
            print("Stopping the script.")
            break
        except Exception as e:
            print(f"Error in monitoring folder: {str(e)}")

if __name__ == "__main__":
    print(f"Monitoring folder: {FOLDER_PATH}")
    monitor_and_upload(FOLDER_PATH)
