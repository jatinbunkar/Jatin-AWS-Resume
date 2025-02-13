# Serverless EC2 Instance Scheduler for Company Working Hours

## Scenario :

In some companies, there is no need to run their EC2 instances 24/7; they require instances to operate during specific time periods, such as company working hours, from 8:00 AM in the morning to 5:00 PM in the evening. To address this scenario, I will implement two Lambda functions responsible for starting and stopping instances. These Lambda functions will be triggered by two CloudWatch Events in the morning and evening. This solution is fully serverless.

## Architecture diagram:

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image1.png" alt="Screenshot of project1image1">
</p>


## **Steps :**

### **Step 1 :**

1. Navigate to the EC2 Console.
2. Lunch an Instance

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image2.png" alt="Screenshot of project1image2">
</p>



### **Step 2 :**

**Creating the Policy :**

1. Navigate to the IAM Console.
2. Click on "Policies" and then Click on "Create policy"

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image3.png" alt="Screenshot of project1image3">
</p>

5. Now we have created a policy for starting instances. We also need to create a policy for stopping the instances. This is because we are going to create two Lambda functions: one for starting and one for stopping the instances. Each function will have its own role, and we will attach these two policies to their respective roles.
6. Now we are going to repeat the same steps for Creating Stopping Policy also.
7. Everything is same , Except Actions because we are going to stop the instance.
8. The Actions are DescribeInstances , StopInstances .
9. Keep your Plolicy name as "stop-ec2-instance".

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image4.png" alt="Screenshot of project1image4">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image5.png" alt="Screenshot of project1image5">
</p>


### **Step 3 :**

**Creating the Lambda functions :**

1. Navigate to the lambda Console.
2. Follow the Outlined steps below.

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image6.png" alt="Screenshot of project1image6">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image7.png" alt="Screenshot of project1image7">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image8.png" alt="Screenshot of project1image8">
</p>



Now Edit Configuration:

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image9.png" alt="Screenshot of project1image9">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image10.png" alt="Screenshot of project1image10">
</p>

Let's Add Policy Created before:

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image11.png" alt="Screenshot of project1image11">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image12.png" alt="Screenshot of project1image12">
</p>


Permission addded Successfully.

Stopped Instance: 

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image13.png" alt="Screenshot of project1image13">
</p>

Test the Lambda function:

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image14.png" alt="Screenshot of project1image14">
</p>

EC2 Instance started:

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image15.png" alt="Screenshot of project1image15">
</p>




3. Now we Created alambda function for Starting Instance.
4. We have to Reapeat the same steps again to Create a Lambda function for Stopping Instance , Keep your lambda function name as "Stop-EC2-demo".
5. The only changes we have to make are to replace the default code with the 'stop-ec2-instance.py' code and attach the policy we created for stopping instances to the role of this Lambda function.

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image16.png" alt="Screenshot of project1image16">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image17.png" alt="Screenshot of project1image17">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image18.png" alt="Screenshot of project1image18">
</p>



Edit Configuration:


<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image19.png" alt="Screenshot of project1image19">
</p>

Add Policy created for stoping the instance:
<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image20.png" alt="Screenshot of project1image20">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image21.png" alt="Screenshot of project1image21">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image22.png" alt="Screenshot of project1image22">
</p>

Test:
<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image23.png" alt="Screenshot of project1image23">
</p>

EC2 Instance is Stopping:
<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image24.png" alt="Screenshot of project1image24">
</p>

6. As demonstrated above, when I test my Python code, it runs successfully and stops the instance.
7. Now, we are ready to proceed and create schedules for this functions.

### **Step 5 :**

**Creating the Schedules Using Cloud Watch :**

1. Navigate to the Cloud Watch Console.
2. Follow the Outlined Steps below.

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image25.png" alt="Screenshot of project1image25">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image26.png" alt="Screenshot of project1image26">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image27.png" alt="Screenshot of project1image27">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image28.png" alt="Screenshot of project1image28">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image29.png" alt="Screenshot of project1image29">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image30.png" alt="Screenshot of project1image30">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image31.png" alt="Screenshot of project1image31">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image32.png" alt="Screenshot of project1image32">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image33.png" alt="Screenshot of project1image33">
</p>

00 8 ? JAN-DEC MON-FRI 2024

3. We have now created a schedule for starting the instance every mond-fri at 8:00 AM.
4. Next, we need to create a schedule for stopping instances.
5. To create the schedule for stopping instances, follow the same steps as for starting instance scheduling with a few changes, Keep your rule name as "stop-ec2-instance".
6. The changes include modifying the scheduled time and selecting the appropriate scheduling function.
7. We need to change the schedule time to 17:00 because it will stop the Lambda function at 17:00 IST (5:00 PM) & Days.

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image34.png" alt="Screenshot of project1image34">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image35.png" alt="Screenshot of project1image35">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image36.png" alt="Screenshot of project1image36">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image37.png" alt="Screenshot of project1image37">
</p>

<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image38.png" alt="Screenshot of project1image38">
</p>

00 17 ? JAN-DEC MON-FRI 2024

Schedules:
<p align="center">
  <img src="https://github.com/jatinbunkar/Jatin-AWS-Resume/blob/cc4e2916483f59feb76b63427418e8322f67bf85/Project/Photos/project1image39.png" alt="Screenshot of project1image39">
</p>
