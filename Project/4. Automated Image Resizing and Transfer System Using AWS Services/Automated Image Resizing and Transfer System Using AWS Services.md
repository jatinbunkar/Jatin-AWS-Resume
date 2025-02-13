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

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image1.png" alt="Screenshot of project4image1">
</p>

## **Steps :**

## **Step 1 :**

## Creating Source and Designation s3 Buckets :

1. Navigate to the S3 Console.
2. Follow the Outlined Steps below.

Bucket: image-initial-upload

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image2.png" alt="Screenshot of project4image2">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image3.png" alt="Screenshot of project4image3">
</p>

Bucket: image-compressed

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image3.png" alt="Screenshot of project4image3">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image4.png" alt="Screenshot of project4image4">
</p>

### Buckets:

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image5.png" alt="Screenshot of project4image5">
</p>

3. As you can see above , I created two buckets one is Source bucket and another one is Destination bucket.

## **Step 2 :**

## Creating the SNS Notification :

1. Navigate to the SNS console.
2. Follow the Outlined Steps below.

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image6.png" alt="Screenshot of project4image6">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image7.png" alt="Screenshot of project4image7">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image8.png" alt="Screenshot of project4image8">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image9.png" alt="Screenshot of project4image9">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image10.png" alt="Screenshot of project4image10">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image11.png" alt="Screenshot of project4image11">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image12.png" alt="Screenshot of project4image12">
</p>

3. Scroll down and Click "Create subscription"
4. After this , you will receive some mail for Subscription Confirmation and you have to confirm that.

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image13.png" alt="Screenshot of project4image13">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image14.png" alt="Screenshot of project4image14">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image15.png" alt="Screenshot of project4image15">
</p>


## Step 3 :

## **Creating the Lambda :**

1. Navigate to the Lambda Console.
2. Follow the Outlined steps below.

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image16.png" alt="Screenshot of project4image16">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image17.png" alt="Screenshot of project4image17">
</p>

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

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image18.png" alt="Screenshot of project4image18">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image19.png" alt="Screenshot of project4image19">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image20.png" alt="Screenshot of project4image20">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image21.png" alt="Screenshot of project4image21">
</p>

5. Now navigate to the Lambda Console and follow the steps below.

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image22.png" alt="Screenshot of project4image22">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image23.png" alt="Screenshot of project4image23">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image24.png" alt="Screenshot of project4image24">
</p>

6. Now we have to trigger the function.

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image25.png" alt="Screenshot of project4image25">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image26.png" alt="Screenshot of project4image26">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image27.png" alt="Screenshot of project4image27">
</p>


7. Now we have to go to code section , and scroll down to layers.
8. We have to add layer .
9. May be you can think , why ?
10. It's because for resize the image we upload in our source S3 bucket , We need a python library called pillow in our code to resize the image . We can manually add Pillow library also, But it's very time consuming and you have to do lot more , Instead of manually adding pillow library we are going to use layers for Some easy action.
11. Follow the outlined Steps below.


<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image28.png" alt="Screenshot of project4image28">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image29.png" alt="Screenshot of project4image29">
</p>

12.You can copy the arn from below.

    - arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p39-pillow:1


<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image30.png" alt="Screenshot of project4image30">
</p>


13. After done all the actions above , now we can test our code.

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image31.png" alt="Screenshot of project4image31">
</p>

## **Step 4 :**

## **Results :**

1. Navigate to the S3 Console.
2. Upload Some images in Source Bucket.

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image32.png" alt="Screenshot of project4image32">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image33.png" alt="Screenshot of project4image33">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image34.png" alt="Screenshot of project4image34">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image35.png" alt="Screenshot of project4image35">
</p>


## Email Notification

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project4image36.png" alt="Screenshot of project4image36">
</p>

## Successfully resized and sent the notification.
