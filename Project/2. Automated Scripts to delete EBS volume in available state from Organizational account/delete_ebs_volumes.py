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
