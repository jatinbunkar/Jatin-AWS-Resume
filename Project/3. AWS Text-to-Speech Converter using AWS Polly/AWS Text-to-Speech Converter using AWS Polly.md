# **AWS Text-to-Speech Converter using AWS Polly**

## **Project Description:**

AWS services to convert text files (such as blog posts, articles, newsletters, or book excerpts) into speech. This is particularly useful for creating audio versions of written content, making it accessible to a wider audience, including those who prefer listening over reading.

## **Use Cases:**

  -  Learning: Enables users to listen to educational materials, enhancing learning experiences.
  -  Content Distribution: Offers an additional medium for content consumption, increasing engagement.
  -  Convenience: Allows users to listen to articles or books while multitasking, such as during commutes or workouts.
  -  Content Accessibility: Provides audio versions of written content for visually impaired users.

## **Architecture Diagram:**

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project3image1.png" alt="Screenshot of project3image1">
</p>

## **Steps:**

* Step 1: Set Up an AWS Account 
* Step 2: Create two S3 Buckets (Source S3 Bucket Name: jatin-polly-source-bucket, Destination S3 Bucket Name: jatin-polly-destination-bucket) 

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project3image2.png" alt="Screenshot of project3image2">
</p>

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

  <p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project3image3.png" alt="Screenshot of project3image3">
</p>


* Step 4: Create an IAM Role (IAM Role Name: jatin-polly-lambda-role) and attach jatin-polly-lambda-policy and AWSLambdaBasicExecutionRole Policies
* Step 5: Create and Configure the Lambda Function (Lambda Function Name: TextToSpeechFunction)
  - Set the runtime to Python 3.8.
  - Set the execution role with necessary permissions for S3 and Polly. (Step 4)
  - Add Environment Variables (`SOURCE_BUCKET`: Name of your source S3 bucket and `DESTINATION_BUCKET`: Name of your destination S3 bucket.
* Step 6: Configure S3 Event Notification
  - Set up an event notification in the source S3 bucket to trigger the Lambda function on new object creation events with the `.txt` suffix.

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project3image4.png" alt="Screenshot of project3image4">
</p>


* Step 7: Write Lambda Function Code


<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project3image5.png" alt="Screenshot of project3image5">
</p>

* Step 8: Test the System
