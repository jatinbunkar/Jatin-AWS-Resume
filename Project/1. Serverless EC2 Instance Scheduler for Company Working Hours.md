# Serverless EC2 Instance Scheduler for Company Working Hours

## Scenario :

In some companies, there is no need to run their EC2 instances 24/7; they require instances to operate during specific time periods, such as company working hours, from 8:00 AM in the morning to 5:00 PM in the evening. To address this scenario, I will implement two Lambda functions responsible for starting and stopping instances. These Lambda functions will be triggered by two CloudWatch Events in the morning and evening. This solution is fully serverless.

## Architecture diagram:

<img width="607" alt="image" src="https://github.com/user-attachments/assets/b3656440-8799-4fee-a27c-84dc0b0ba878" />

## **Steps :**

### **Step 1 :**

1. Navigate to the EC2 Console.
2. Lunch an Instance

<img width="903" alt="image" src="https://github.com/user-attachments/assets/4484a0c1-d9fd-4401-9b0e-39ab24ba36ce" />


### **Step 2 :**

**Creating the Policy :**

1. Navigate to the IAM Console.
2. Click on "Policies" and then Click on "Create policy"

<img width="1429" alt="image" src="https://github.com/user-attachments/assets/11ec082b-61e0-411b-b32a-e6b690225569" />

5. Now we have created a policy for starting instances. We also need to create a policy for stopping the instances. This is because we are going to create two Lambda functions: one for starting and one for stopping the instances. Each function will have its own role, and we will attach these two policies to their respective roles.
6. Now we are going to repeat the same steps for Creating Stopping Policy also.
7. Everything is same , Except Actions because we are going to stop the instance.
8. The Actions are DescribeInstances , StopInstances .
9. Keep your Plolicy name as "stop-ec2-instance".

<img width="1430" alt="image" src="https://github.com/user-attachments/assets/d05136f3-d2fa-4d90-8a52-dc6597365b54" />


<img width="1211" alt="image" src="https://github.com/user-attachments/assets/3b99e05f-5eb8-4919-a60a-72e48801b9fc" />


### **Step 3 :**

**Creating the Lambda functions :**

1. Navigate to the lambda Console.
2. Follow the Outlined steps below.

<img width="1219" alt="image" src="https://github.com/user-attachments/assets/33576b15-558b-426f-b514-ab62d5e03760" />

<img width="1210" alt="image" src="https://github.com/user-attachments/assets/e46ffd14-add8-4ec3-b106-ec2ef97909bd" />

<img width="1060" alt="image" src="https://github.com/user-attachments/assets/78c83ebb-9e55-4ca3-9745-806cc3bf0e5b" />

Now Edit Configuration:

<img width="1224" alt="image" src="https://github.com/user-attachments/assets/7e2ca2dc-3844-4df9-924e-9abd15437240" />

<img width="1212" alt="image" src="https://github.com/user-attachments/assets/2b8d8e44-546c-4205-bc90-5ec0babe9d97" />

Let's Add Policy Created before:

<img width="979" alt="image" src="https://github.com/user-attachments/assets/abb6a9bb-45be-4e4f-85f3-7b52a4f26fe8" />

<img width="978" alt="image" src="https://github.com/user-attachments/assets/68057302-69ee-44c5-a645-268af7777366" />

Permission addded Successfully.




Stopped Instance: 
<img width="1226" alt="image" src="https://github.com/user-attachments/assets/e58bb76e-856c-44d1-8a91-608b83d92db2" />

Test the Lambda function:
<img width="1207" alt="image" src="https://github.com/user-attachments/assets/0de0a877-1ddf-4f07-822b-daa9526ef799" />

EC2 Instance started:
<img width="1207" alt="image" src="https://github.com/user-attachments/assets/b64df9ed-609a-4a04-9121-d0cf2914918f" />

3. Now we Created alambda function for Starting Instance.
4. We have to Reapeat the same steps again to Create a Lambda function for Stopping Instance , Keep your lambda function name as "Stop-EC2-demo".
5. The only changes we have to make are to replace the default code with the 'stop-ec2-instance.py' code and attach the policy we created for stopping instances to the role of this Lambda function.

<img width="1212" alt="image" src="https://github.com/user-attachments/assets/bbd8d893-9ae8-4e39-b07b-824a905ef8f2" />

<img width="1213" alt="image" src="https://github.com/user-attachments/assets/25219308-d58c-405f-b9ae-64c22e810176" />

<img width="1216" alt="image" src="https://github.com/user-attachments/assets/d781da95-303b-4a10-b208-aff76c64c0a5" />

Edit Configuration:
<img width="1210" alt="image" src="https://github.com/user-attachments/assets/bfc3a524-7bfa-4c15-bd3f-953fc0819ee4" />

Add Policy created for stoping the instance:
<img width="976" alt="image" src="https://github.com/user-attachments/assets/0e7cafc1-ff7e-42d4-a539-f99377e868f1" />

<img width="1330" alt="image" src="https://github.com/user-attachments/assets/4ebc0f90-ddbf-4927-89c2-82a952f3b076" />

<img width="975" alt="image" src="https://github.com/user-attachments/assets/83543409-e788-4eff-a2be-54e384f5326a" />

Test:
<img width="1227" alt="image" src="https://github.com/user-attachments/assets/c15057a4-17da-4995-90ff-95be22dfb631" />

EC2 Instance is Stopping:
<img width="1225" alt="image" src="https://github.com/user-attachments/assets/d988be5f-e05b-4e12-aec2-484b62662845" />

6. As demonstrated above, when I test my Python code, it runs successfully and stops the instance.
7. Now, we are ready to proceed and create schedules for this functions.

### **Step 5 :**

**Creating the Schedules Using Cloud Watch :**

1. Navigate to the Cloud Watch Console.
2. Follow the Outlined Steps below.

<img width="1432" alt="image" src="https://github.com/user-attachments/assets/8f17401e-0879-4873-a669-bb3670769bac" />

<img width="1215" alt="image" src="https://github.com/user-attachments/assets/47f3d4e7-b15b-49cd-bc7e-b4c67e6d3b62" />

<img width="1353" alt="image" src="https://github.com/user-attachments/assets/f417217c-87a9-4187-bc10-75dcb948fd28" />


<img width="1349" alt="image" src="https://github.com/user-attachments/assets/137a86dd-6d58-4f6d-9506-b64e02cbd1b8" />

<img width="1341" alt="image" src="https://github.com/user-attachments/assets/6e7a9c2b-2af6-4cfe-91f6-cbf50a63a251" />

<img width="1338" alt="image" src="https://github.com/user-attachments/assets/4a00aa77-0066-485e-9e26-3b5e267ac712" />

<img width="1350" alt="image" src="https://github.com/user-attachments/assets/c7b126bd-5fd5-4495-bb7a-d3e332001f03" />

<img width="1353" alt="image" src="https://github.com/user-attachments/assets/53ca12b9-caf9-4521-a2ba-2ab4d7d6884c" />

<img width="1440" alt="image" src="https://github.com/user-attachments/assets/110a4339-8549-4ef0-9275-1a1c5283e95a" />

00 8 ? JAN-DEC MON-FRI 2024

3. We have now created a schedule for starting the instance every mond-fri at 8:00 AM.
4. Next, we need to create a schedule for stopping instances.
5. To create the schedule for stopping instances, follow the same steps as for starting instance scheduling with a few changes, Keep your rule name as "stop-ec2-instance".
6. The changes include modifying the scheduled time and selecting the appropriate scheduling function.
7. We need to change the schedule time to 17:00 because it will stop the Lambda function at 17:00 IST (5:00 PM) & Days.

<img width="1339" alt="image" src="https://github.com/user-attachments/assets/f63dee18-b420-418e-bb09-a5db49ce5a0b" />

<img width="1351" alt="image" src="https://github.com/user-attachments/assets/e58f5758-1d50-4e05-a2b5-61a7d6b8b399" />

<img width="1337" alt="image" src="https://github.com/user-attachments/assets/c9528578-f7d8-4971-b398-007ec0ea7906" />

<img width="1423" alt="image" src="https://github.com/user-attachments/assets/6eb15d4b-91dd-4e98-9eb6-c0e5351280dc" />

<img width="1438" alt="image" src="https://github.com/user-attachments/assets/3e9acc23-206d-47d1-892c-f1f0160e76b5" />

00 17 ? JAN-DEC MON-FRI 2024

Schedules:
<img width="1205" alt="image" src="https://github.com/user-attachments/assets/f10e82fd-e205-4a1a-97a6-b538354c8bc5" />
