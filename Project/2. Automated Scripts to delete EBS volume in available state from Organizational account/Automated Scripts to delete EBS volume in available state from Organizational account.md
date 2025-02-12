# **Automated Script to Delete EBS Volumes in Available State**

This project contains automated scripts and policies to delete EBS volumes in the available state across AWS organizational accounts. The process involves cross-account roles, specific IAM policies, and a Python script for execution.

---

## **Table of Contents**
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [IAM Policies and Roles](#iam-policies-and-roles)
   - [Root Account Policies](#root-account-policies)
   - [Member Account Policies](#member-account-policies)
4. [Python Script](#python-script)
5. [Cloud Shell Script](#cloud-shell-script)
6. [Output](#output)
7. [Notes](#notes)

---

## **Overview**

This script identifies and deletes unattached EBS volumes (status: available) across all accounts in an AWS Organization. It also generates a CSV report with details of the deleted volumes, including Account ID, Volume ID, Region, and Size.

### **EBS Volumes**
- **Attached Volumes:** EBS volumes actively used by an EC2 instance.
- **Available Volumes:** Unattached EBS volumes incurring unnecessary costs. This script targets these volumes to optimize resource utilization and reduce costs.

---

## **Prerequisites**

1. AWS CLI configured with necessary permissions.
2. Python 3.x installed with the `boto3` library.
3. Administrator access to the AWS Organization’s root account.
4. Cross-account IAM roles configured for the organizational structure.

---

## **IAM Policies and Roles**

### **Root Account**

#### **Role Name: CrossAccountEC2DeleteRole**

##### **Policy for Volume Deletion**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DeleteVolume",
        "ec2:DescribeVolumes",
        "ec2:DetachVolume"
      ],
      "Resource": "*"
    }
  ]
}
```

##### **Trusted Policy**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::87938XXXXXXX:user/Jatin"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### **Member Account Policies**

#### **Policy for Volume Deletion**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DeleteVolume",
        "ec2:DescribeVolumes",
        "ec2:DetachVolume"
      ],
      "Resource": "*"
    }
  ]
}
```
#### **Trust Policy**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<Root Account ID>:user/<User Name>"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

---


## **Python Script**

The Python script, `delete_ebs_volumes.py`, performs the following tasks:

- List all accounts in the AWS Organization.
- Assume a cross-account role for each account.
- Identify and delete all available EBS volumes in specified regions.
- Log deleted volume details in a CSV file (`ebs_volumes_report.csv`).

```python
import boto3
import csv
from botocore.exceptions import ClientError

def list_accounts_in_org():
    """List all accounts in the AWS Organization."""
    org_client = boto3.client('organizations')
    accounts = []
    response = org_client.list_accounts()
    accounts.extend(response['Accounts'])
    while 'NextToken' in response:
        response = org_client.list_accounts(NextToken=response['NextToken'])
        accounts.extend(response['Accounts'])
    return [account['Id'] for account in accounts]

def assume_role(account_id, role_name):
    """Assume the cross-account role and return the temporary credentials."""
    sts_client = boto3.client('sts')
    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    try:
        response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName="DeleteEBSVolumesSession"
        )
        credentials = response['Credentials']
        return credentials
    except ClientError as e:
        print(f"Error assuming role for account {account_id}: {e}")
        return None

def get_specified_regions():
    """Return a list of specified regions for EBS volume deletion."""
    return ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2']

def delete_available_volumes(ec2_client, account_id, region, writer):
    """Delete all available EBS volumes in the specified region and record their details in a CSV file."""
    try:
        # Fetch available EBS volumes
        volumes = ec2_client.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
        for volume in volumes['Volumes']:
            volume_id = volume['VolumeId']
            volume_size = volume['Size']
            availability_zone = volume['AvailabilityZone']
            region = availability_zone[:-1]
            print(f"Account {account_id}: Found available Volume {volume_id} in {region} ({availability_zone}) - Size: {volume_size} GB")
            writer.writerow({
                'Account ID': account_id,
                'Volume ID': volume_id,
                'Size (GB)': volume_size,
                'Region': region,
                'Status': 'Available'
            })
            # Delete the volume
            print(f"Deleting available Volume {volume_id}...")
            ec2_client.delete_volume(VolumeId=volume_id)
    except ClientError as e:
        print(f"Error deleting volumes for account {account_id}: {e}")

def main():
    role_name = "CrossAccountEC2DeleteRole"
    accounts = list_accounts_in_org()
    regions = get_specified_regions()
    with open('ebs_volumes_report.csv', mode='w', newline='') as file:
        fieldnames = ['Account ID', 'Volume ID', 'Size (GB)', 'Region', 'Status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for account_id in accounts:
            print(f"\nProcessing account {account_id}...")
            credentials = assume_role(account_id, role_name)
            if credentials:
                for region in regions:
                    print(f"\nProcessing region {region} for account {account_id}...")
                    ec2_client = boto3.client(
                        'ec2',
                        aws_access_key_id=credentials['AccessKeyId'],
                        aws_secret_access_key=credentials['SecretAccessKey'],
                        aws_session_token=credentials['SessionToken'],
                        region_name=region
                    )
                    delete_available_volumes(ec2_client, account_id, region, writer)

if __name__ == "__main__":
    main()
```

---

## **Cloud Shell Script**

To execute the script in AWS Cloud Shell:

1. **Create a Python File**
   - Open AWS Cloud Shell.
   - Create a new Python file:
     ```bash
     touch ebsvolumescript.py
     ```

2. **Copy and Edit the Code**
   - Open the file in an editor:
     ```bash
     nano ebsvolumescript.py
     ```
   - Paste the Python script provided above into the file and save it.
  
3. **Run the File**
   - Execute the script:
     ```bash
     python ebsvolumescript.py
     ```
The script will identify and delete available EBS volumes and generate a report `ebs_volumes_report.csv` in the current directory.

---

## **Output**

The script generates a CSV report with the following columns:
- **Account ID**
- **Volume ID**
- **Size (GB)**
- **Region**
- **Status**

---

## **Notes**

- The `CrossAccountEC2DeleteRole` must be created in each member account with the defined policies.
- Ensure the trusted entity for the cross-account role is correctly set to the root account.
- Modify the `get_specified_regions()` function in the script if additional regions need to be included.

---
