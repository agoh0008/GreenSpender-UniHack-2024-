import boto3
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from send_api import analyze_image_and_update_json
# Initialize the S3 client
session = boto3.Session(profile_name='profile1')
s3 = session.client('s3')

# Define the S3 bucket name and the local folder path
bucket_name = 'image-storage--testing'
local_folder = r'D:\Projects\Hackathon1\pictures'
# Define the path to the LINK.txt file
link_file = os.path.join(local_folder, 'LINK.txt')

# Function to upload an image to S3 and return its presigned URL
def upload_image_to_s3(image_file, bucket_name):
    # Generate the key name for the image within the S3 bucket
    key_name = os.path.join('images', os.path.basename(image_file))
    # Upload the image to S3
    try:
        with open(image_file, 'rb') as image_data:
            s3.upload_fileobj(image_data, bucket_name, key_name)
        print(f"Image '{image_file}' uploaded successfully to S3!")

        # Generate a presigned URL for the uploaded image
        url = s3.generate_presigned_url('get_object',
                                        Params={'Bucket': bucket_name, 'Key': key_name},
                                        ExpiresIn=3600) # URL expires in 1 hour
        return url
    except FileNotFoundError:
        print(f"Error uploading image '{image_file}' to S3: No such file or directory")
    except Exception as e:
        print(f"Error uploading image '{image_file}' to S3:", e)

# Event handler class to monitor changes in the local folder
class ImageUploadHandler(FileSystemEventHandler):
    def _init_(self):
        self.uploaded_files = set()

    def on_created(self, event):
        if event.is_directory:
            return
        filename = event.src_path
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            time.sleep(1)  # Wait a bit for the file to be fully written
            presigned_url = upload_image_to_s3(filename, bucket_name)
            if presigned_url:
                with open(link_file, 'a') as f:
                    f.write(presigned_url + '\n')
                analyze_image_and_update_json(presigned_url, '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')


# Function to start monitoring the local folder for image uploads
def start_monitoring():
    event_handler = ImageUploadHandler()
    observer = Observer()
    observer.schedule(event_handler, local_folder, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



# Start monitoring the local folder
start_monitoring()