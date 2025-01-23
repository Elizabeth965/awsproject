import boto3
import os
import time

# Configuration
BUCKET_NAME = 'secure-backup-system'  # Replace with your bucket name
DOWNLOAD_FOLDER = '/Users/ms.elizabethlisamondol/Desktop/restored_files/'  # Local folder to save restored files
CHECK_INTERVAL = 10  # Time in seconds to wait between checks

# Initialize S3 client
s3 = boto3.client('s3')

# Keep track of downloaded files
downloaded_files = set()

def download_file(file_name, download_path):
    """Downloads a single file from S3."""
    try:
        s3.download_file(BUCKET_NAME, file_name, download_path)
        print(f"{file_name} downloaded successfully to {download_path}")
        return True
    except Exception as e:
        print(f"Error downloading file {file_name}: {str(e)}")
        return False

def restore_from_s3():
    """Continuously monitors S3 and restores new files."""
    global downloaded_files
    while True:
        try:
            # List all files in the bucket
            objects = s3.list_objects_v2(Bucket=BUCKET_NAME)
            if 'Contents' in objects:
                for obj in objects['Contents']:
                    file_name = obj['Key']  # Name of the file in S3
                    download_path = os.path.join(DOWNLOAD_FOLDER, file_name)  # Local path

                    # Skip if file is already downloaded
                    if file_name in downloaded_files:
                        continue

                    # Create local folder if it doesn't exist
                    os.makedirs(os.path.dirname(download_path), exist_ok=True)

                    # Download the file
                    if download_file(file_name, download_path):
                        downloaded_files.add(file_name)  # Mark as downloaded

            print(f"Waiting for {CHECK_INTERVAL} seconds before checking S3 again...")
            time.sleep(CHECK_INTERVAL)  # Wait before rechecking
        except KeyboardInterrupt:
            print("Stopping the restore script.")
            break
        except Exception as e:
            print(f"Error in restore process: {str(e)}")

if __name__ == "__main__":
    print(f"Monitoring S3 bucket: {BUCKET_NAME} for new files...")
    restore_from_s3()
