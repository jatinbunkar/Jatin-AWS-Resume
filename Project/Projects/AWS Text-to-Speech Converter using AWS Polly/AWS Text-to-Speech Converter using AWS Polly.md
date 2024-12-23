# **AWS Text-to-Speech Converter using AWS Polly**

## **Project Description:**

AWS services to convert text files (such as blog posts, articles, newsletters, or book excerpts) into speech. This is particularly useful for creating audio versions of written content, making it accessible to a wider audience, including those who prefer listening over reading.

## **Use Cases:**

  -  Learning: Enables users to listen to educational materials, enhancing learning experiences.
  -  Content Distribution: Offers an additional medium for content consumption, increasing engagement.
  -  Convenience: Allows users to listen to articles or books while multitasking, such as during commutes or workouts.
  -  Content Accessibility: Provides audio versions of written content for visually impaired users.

## **Architecture Diagram:**

<img width="753" alt="image" src="https://github.com/user-attachments/assets/238b0329-7014-40c2-bc99-8025223f6ce1" />

## **Steps:**

* Step 1: Set Up an AWS Account 
* Step 2: Create two S3 Buckets (Source S3 Bucket Name: jatin-polly-source-bucket, Destination S3 Bucket Name: jatin-polly-destination-bucket) 

<img width="1440" alt="image" src="https://github.com/user-attachments/assets/3236c092-2046-402a-be37-ac1f11d8b289" />

* Step 3: Create an IAM Policy (IAM Policy Name: jatin-polly-lambda-policy) 

   Policy Defination:

  ```bash
  {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": [
                "arn:aws:s3:::jatin-polly-source-bucket/*",
                "arn:aws:s3:::jatin-polly-destination-bucket/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "polly:SynthesizeSpeech"
            ],
            "Resource": "*"
        }
    ]
  }

  ```

  <img width="1440" alt="image" src="https://github.com/user-attachments/assets/76b37d7e-73b9-4093-92fa-5949080e4313" />


* Step 4: Create an IAM Role (IAM Role Name: jatin-polly-lambda-role) and attach jatin-polly-lambda-policy and AWSLambdaBasicExecutionRole Policies
* Step 5: Create and Configure the Lambda Function (Lambda Function Name: TextToSpeechFunction)
  - Set the runtime to Python 3.8.
  - Set the execution role with necessary permissions for S3 and Polly. (Step 4)
  - Add Environment Variables (`SOURCE_BUCKET`: Name of your source S3 bucket and `DESTINATION_BUCKET`: Name of your destination S3 bucket.
* Step 6: Configure S3 Event Notification
  - Set up an event notification in the source S3 bucket to trigger the Lambda function on new object creation events with the `.txt` suffix.
 
<img width="1439" alt="image" src="https://github.com/user-attachments/assets/bbd1224e-25ac-4745-96b2-9e71f2ed99c2" />


* Step 7: Write Lambda Function Code

<img width="1440" alt="image" src="https://github.com/user-attachments/assets/a91609eb-6cf1-47ea-9e94-434f13e08a97" />

* Step 8: Test the System
