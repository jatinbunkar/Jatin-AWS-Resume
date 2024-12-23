# **Automated Image Resizing and Transfer System Using AWS Services**

## Project Description

This project aims to develop an automated image processing and management system within the AWS ecosystem. The solution is designed to simplify image handling by automatically resizing images and transferring them to a specified storage location, while ensuring stakeholders are notified throughout the process. Key AWS services, including Lambda, S3, and SNS, are leveraged to orchestrate this workflow efficiently.

## Key Features:

1. Image processing automation: Automatically resize and optimize images upon upload.
2. Secure storage: Store processed images in a secure and reliable S3 bucket.
3. Real-time notifications: Receive immediate updates about image processing via SNS.
4. Scalable architecture: Design for scalability to handle image processing demands.
5. Cost-efficient solution: Leverage AWS serverless technologies to minimize operational costs.


## Architecture Diagram

<img width="855" alt="image" src="https://github.com/user-attachments/assets/53b56c17-02a5-4757-829f-8ff428181842" />

## **Steps :**

## **Step 1 :**

## Creating Source and Designation s3 Buckets :

1. Navigate to the S3 Console.
2. Follow the Outlined Steps below.

Bucket: image-initial-upload

<img width="1212" alt="image" src="https://github.com/user-attachments/assets/bb6fca05-19e9-4d9b-9459-5dbba10898cf" />

<img width="1213" alt="image" src="https://github.com/user-attachments/assets/0eb5b55b-0442-48a1-a28d-12f374044015" />

Bucket: image-compressed

<img width="1213" alt="image" src="https://github.com/user-attachments/assets/5e4b311f-a1c8-4f9d-bd97-bddc7e15ff34" />

<img width="1209" alt="image" src="https://github.com/user-attachments/assets/8b788b64-6d77-4504-bf15-3311480c6e9e" />

### Buckets:

<img width="976" alt="image" src="https://github.com/user-attachments/assets/9ba25fe9-2d3c-423b-8a72-7cd3393bcbc5" />

3. As you can see above , I created two buckets one is Source bucket and another one is Destination bucket.

## **Step 2 :**

## Creating the SNS Notification :

1. Navigate to the SNS console.
2. Follow the Outlined Steps below.

<img width="1435" alt="image" src="https://github.com/user-attachments/assets/6a8b14e6-7614-47ea-86a9-df0a133f84de" />

<img width="1321" alt="image" src="https://github.com/user-attachments/assets/760ba102-fb72-477c-b7dc-38f01fcda1c1" />

<img width="1217" alt="image" src="https://github.com/user-attachments/assets/4e419ae9-ed90-4ff8-8588-45b5a0eb0fef" />

<img width="1229" alt="image" src="https://github.com/user-attachments/assets/c03cea2d-0c70-47ba-b8fd-680cda21c70a" />

<img width="980" alt="image" src="https://github.com/user-attachments/assets/42c20d04-0bd4-4d1e-8e79-579237cc2ccc" />

<img width="1188" alt="image" src="https://github.com/user-attachments/assets/0137e8a3-d5a3-4af7-94a9-dab5e9765ce7" />

<img width="983" alt="image" src="https://github.com/user-attachments/assets/10ee639c-a666-470e-8637-922e67095878" />

3. Scroll down and Click "Create subscription"
4. After this , you will receive some mail for Subscription Confirmation and you have to confirm that.

<img width="986" alt="image" src="https://github.com/user-attachments/assets/e2a19931-1994-4eec-9949-0fece540bfcd" />

<img width="616" alt="image" src="https://github.com/user-attachments/assets/0987c14b-0383-488b-9349-aef9292ac6f1" />

<img width="979" alt="image" src="https://github.com/user-attachments/assets/3b767ae3-c7fc-4fad-978b-daa3f70b397a" />


## Step 3 :

## **Creating the Lambda :**

1. Navigate to the Lambda Console.
2. Follow the Outlined steps below.

<img width="1217" alt="image" src="https://github.com/user-attachments/assets/507419fe-3e70-4ae4-96f9-63437ba5e980" />

<img width="1214" alt="image" src="https://github.com/user-attachments/assets/4e753d83-25f7-4e79-92e4-c4a8015a67a3" />

3. Now replace the default code with the image-resizing-s3.py or below code and deploy the changes , Don't test the code now we have to do some more actions before testing.

```python
import os
import boto3
from PIL import Image
from io import BytesIO

# Initialize AWS clients
s3 = boto3.client('s3')
sns = boto3.client('sns')

# Define the S3 buckets and SNS topic
bucket_1 = 'image-initial-upload' # your-source-bucket
bucket_2 = 'image-compressed' # your-destination-bucket
sns_topic_arn = 'arn:aws:sns:us-east-1:502433561161:image-resizing-topic' # your-sns-topic

def lambda_handler(event, context):
    if 'Records' in event:
        # Handle S3 batch event
        for record in event['Records']:
            handle_s3_record(record)
    else:
        # Handle single S3 event
        handle_s3_record(event)

def handle_s3_record(record):
    # Ensure the event record structure is correct
    if 's3' in record and 'bucket' in record['s3'] and 'name' in record['s3']['bucket'] and 'object' in record['s3'] and 'key' in record['s3']['object']:
        # Get the bucket name and object key from the S3 event record
        source_bucket = record['s3']['bucket']['name']
        object_key = record['s3']['object']['key']

        # Download the file from S3 bucket_1
        response = s3.get_object(Bucket=source_bucket, Key=object_key)
        content_type = response['ContentType']
        image_data = response['Body'].read()

        # Resize and compress the image
        resized_image = resize_and_compress_image(image_data)

        # Upload the resized and compressed image to S3 bucket_2
        destination_key = f"resized/{object_key}"
        s3.put_object(Bucket=bucket_2, Key=destination_key, Body=resized_image, ContentType=content_type)

        # Send a notification to the SNS topic
        message = f"Image {object_key} has been resized and uploaded to {bucket_2}"
        sns.publish(TopicArn=sns_topic_arn, Message=message)
    else:
        # Log an error message if the event record structure is unexpected
        print("Error: Invalid S3 event record structure")


def resize_and_compress_image(image_data, quality=75):
    # Open the image using PIL
    image = Image.open(BytesIO(image_data))

    # Compress the image
    image_io = BytesIO()
    image.save(image_io, format=image.format, quality=quality)

    return image_io.getvalue()
```

4. After that , We have to give some permission for our Lambda Function to do our process (resizing) , For that navigate to the IAM Console and follow the below steps.

<img width="1440" alt="image" src="https://github.com/user-attachments/assets/7e2a6642-6f23-4305-8df1-70d64e4b0bd1" />

<img width="1203" alt="image" src="https://github.com/user-attachments/assets/bddb3351-8f45-4e8e-8b0d-1e782371e1b8" />

<img width="1206" alt="image" src="https://github.com/user-attachments/assets/d7a76c06-ec09-41d0-8e7e-44a9c7027b2a" />

<img width="1438" alt="image" src="https://github.com/user-attachments/assets/e2493c65-1d38-4697-aa5f-06cfeb7ceb23" />

5. Now navigate to the Lambda Console and follow the steps below.

<img width="1218" alt="image" src="https://github.com/user-attachments/assets/0f21bbdd-4e68-4220-80b2-8f1514a506a9" />

<img width="1315" alt="image" src="https://github.com/user-attachments/assets/a43fcb89-d36f-449b-ac99-77eaa9b3e73c" />

<img width="1335" alt="image" src="https://github.com/user-attachments/assets/a21dfa82-d78c-47b9-8791-a31fc137bb9d" />

6. Now we have to trigger the function.

<img width="1006" alt="image" src="https://github.com/user-attachments/assets/8e1b84ed-a823-40bf-9d3b-d3a392685849" />

<img width="1245" alt="image" src="https://github.com/user-attachments/assets/44813fb7-d52a-4c06-a4aa-e18fc9c2ecd6" />

<img width="824" alt="image" src="https://github.com/user-attachments/assets/20f340cf-0eb5-4686-8656-e31cd1c6719e" />

7. Now we have to go to code section , and scroll down to layers.
8. We have to add layer .
9. May be you can think , why ?
10. It's because for resize the image we upload in our source S3 bucket , We need a python library called pillow in our code to resize the image . We can manually add Pillow library also, But it's very time consuming and you have to do lot more , Instead of manually adding pillow library we are going to use layers for Some easy action.
11. Follow the outlined Steps below.


<img width="1262" alt="image" src="https://github.com/user-attachments/assets/88be358d-a59a-43bd-86c2-85154807d6f9" />

<img width="1008" alt="image" src="https://github.com/user-attachments/assets/9330844e-a650-448f-8d03-1b0dd75adace" />


12.You can copy the arn from below.

    - arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p39-pillow:1

<img width="995" alt="image" src="https://github.com/user-attachments/assets/8fc6cb7b-3945-48ac-9631-5a984f501d32" />


13. After done all the actions above , now we can test our code.


<img width="1215" alt="image" src="https://github.com/user-attachments/assets/8dd2b9f2-bde2-413c-ac78-ee0deb96c7c2" />

## **Step 4 :**

## **Results :**

1. Navigate to the S3 Console.
2. Upload Some images in Source Bucket.

<img width="1217" alt="image" src="https://github.com/user-attachments/assets/a5ca4821-d79e-467f-844d-28f8bd7a88c0" />

<img width="1244" alt="image" src="https://github.com/user-attachments/assets/2ee7fb89-868a-43b0-9471-a464fa52e337" />

<img width="1219" alt="image" src="https://github.com/user-attachments/assets/ce9287e0-5b64-49ca-ae13-61ea093ece92" />

<img width="1224" alt="image" src="https://github.com/user-attachments/assets/c85f0455-7156-40e1-8a43-96e8ded346b0" />


## Email Notification

<img width="1101" alt="image" src="https://github.com/user-attachments/assets/b43d0671-b9b7-4b46-9917-de123b16f1c1" />

## Successfully resized and sent the notification.
