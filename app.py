import os
import boto3
import requests

# Get bucket name and URL from environment variables
bucket_name = os.getenv('BUCKET_NAME')
url = os.getenv('URL')

if not bucket_name or not url:
    print("Error: BUCKET_NAME and URL environment variables must be set.")
    exit(1)

access_id = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

if not access_id or not secret_key :
    print("Error: BUCKET_NAME and URL environment variables must be set.")
    exit(1)

# Creating the S3 client 
client = boto3.client('s3')

try:
    # Create the S3 bucket
    response = client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': os.getenv('AWS_DEFAULT_REGION', 'us-east-1')  # Default to 'us-east-1' if not set
        },
        ObjectOwnership='BucketOwnerPreferred'
    )

    # Unblock public access
    client.delete_public_access_block(
        Bucket=bucket_name
    )

    print("Bucket created successfully:", response)
except Exception as e:
    print("Error creating bucket:", e)
    exit(1)

# Getting webpage source code
try:
    response = requests.get(url)
    if response.status_code == 200:
        webpage_content = response.text
    else:
        print("Failed to retrieve the webpage")
        exit(1)
except Exception as e:
    print("Error fetching the webpage:", e)
    exit(1)

# Save the webpage content locally
file_name = "webpage_source.html"
with open(file_name, "w", encoding="utf-8") as file:
    file.write(webpage_content)

# Upload the file to S3
try:
    client.upload_file(
        file_name, bucket_name, file_name,
        ExtraArgs={'ACL': 'public-read', 'ContentType': 'text/html'}
    )
    print(f"File {file_name} uploaded to S3 successfully!")
except Exception as e:
    print(f"Error uploading file to S3: {e}")