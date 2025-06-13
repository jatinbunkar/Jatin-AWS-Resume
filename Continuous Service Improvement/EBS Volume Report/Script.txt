# Import the boto3 SDK for AWS, and other standard libraries
import boto3
import subprocess, csv, os, json
import argparse, logging

# Enable logging to a file with INFO level messages
# This helps us track the script’s progress or debug if something goes wrong
logging.basicConfig(filename='GetVolumeDetailsAllAccountsOU.log', level=logging.INFO)


# Define the Global variables here
# Clear the terminal first (just for a clean view)
subprocess.call (["clear"], shell = True)

# Define CSV column names for the output
field_names = ['Account', 'Volume_Id', 'Volume_Size', 'Availability_Zone',
               'Volume_Type', 'State', 'CreateTime', 'Description', 
               'Owner', 'Team', 'Instance_Id']

# List to collect all volumes’ details
rows = []


# ------------------------------------------------------------------------------
# List all AWS accounts under Organization
# ------------------------------------------------------------------------------
def getallAccounts():
    # Prints a message to show process start
    print('Getting all AWS Accounts')
    accountList = []

    # Create a boto3 Organizations client
    client = boto3.client('organizations')
    paginator = client.get_paginator('list_accounts')

    try:
        # Iterate through all paginated responses.    
        #retrieving large sets of data in batches or “pages” instead of all at once.
        iterator = paginator.paginate()
        for page in iterator:
            for Account in page['Accounts']:
                if Account['Status'] == 'ACTIVE':
                    accountList.append(Account['Id'])  # Store active account IDs
                else:
                    logging.info('Account ' + Account['Id'] + ' is not Active, skipping!')
                    pass
    except Exception as e:
        raise e  # Raise if something goes wrong
    
    return accountList


# ------------------------------------------------------------------------------
# Assume role in another account to enable cross account access
# ------------------------------------------------------------------------------
def assume_role(target_account, role):
    # Acquire STS Client to perform AssumeRole
    sts = boto3.client('sts')
    try:
        # Assume Role in the Target account
        assume_role_object = sts.assume_role(
            RoleArn='arn:aws:iam::' + target_account + ':role/' + role,
            RoleSessionName='AssumingCrossAccountRole'
        )
    except Exception as err:
        logging.error("Error occurred while assuming role: {}".format(err))
        return False
    
    # Store credentials in a dictionary for further usage
    role_dict = dict()
    role_dict['AccessKeyId'] = assume_role_object['Credentials']['AccessKeyId']
    role_dict['SecretAccessKey'] = assume_role_object['Credentials']['SecretAccessKey']
    role_dict['SessionToken'] = assume_role_object['Credentials']['SessionToken']

    return role_dict


# ------------------------------------------------------------------------------
# Retrieve all EC2 regions
# ------------------------------------------------------------------------------
def get_all_regions():
    # EC2 Client without specifying region
    ec2 = boto3.client('ec2')
    # List all EC2 regions
    regions = ec2.describe_regions()['Regions']

    return [region['RegionName'] for region in regions]


# ------------------------------------------------------------------------------
# Retrieve all volumes in a particular account & region
# ------------------------------------------------------------------------------
def getallvolumes(act, client, region):
    logging.info(f"Describing volumes for account {act} in region {region}")

    response = client.describe_volumes(MaxResults=500)
    volumeList = response.get("Volumes", [])
    logging.info(f'Number of Volumes fetched in region {region}: {len(volumeList)}')
    
    if len(volumeList) != 0:
        for vol in volumeList:
            if "Tags" in vol:
                tags = vol['Tags']
            else:
                tags = None
            # Store this volume's details in our data structure
            build_rows_dictionary(act, vol['VolumeId'], vol['Size'], 
                                   vol['AvailabilityZone'], vol['VolumeType'], 
                                   vol['State'], vol['CreateTime'], tags)
        
        # Handle pagination if there are more volumes
        while('NextToken' in response):
            response = client.describe_volumes(MaxResults=500, NextToken=response['NextToken'])

            volumeList = response.get("Volumes", [])
            logging.info(f'Number of Volumes fetched in region {region}: {len(volumeList)}')
            if len(volumeList) != 0:
                for vol in volumeList:
                    if "Tags" in vol:
                        tags = vol['Tags']
                    else:
                        tags = None
                    build_rows_dictionary(act, vol['VolumeId'], vol['Size'], 
                                           vol['AvailabilityZone'], vol['VolumeType'], 
                                           vol['State'], vol['CreateTime'], tags)
    else:
        logging.info(f'No volumes found for account {act} in region {region}')


# ------------------------------------------------------------------------------
# Store volume details in a row
# ------------------------------------------------------------------------------
def build_rows_dictionary(account, volume_id, volume_size, availability_zone, volume_type, state, create_time, tags):
    row_dict = {}
    row_dict["Account"] = account
    row_dict["Volume_Id"] = volume_id
    row_dict["Volume_Size"] = volume_size
    row_dict["Availability_Zone"] = availability_zone
    row_dict["Volume_Type"] = volume_type
    row_dict["State"] = state
    row_dict["CreateTime"] = create_time
    
    if tags:
        for x in tags:
            if x['Key'] == "Owner":
                row_dict["Owner"] = x['Value']
            elif x['Key'] == "Team":
                row_dict["Team"] = x['Value']
            elif x['Key'] == "instance_id":
                row_dict["Instance_Id"] = x['Value']

    # Finally, add this row to the main list
    rows.append(row_dict)


# ------------------------------------------------------------------------------
# Write all collected data to CSV
# ------------------------------------------------------------------------------
def write_csv(filepath):
    # Open CSV for writing
    with open(filepath, 'w') as f:
        csv_writer = csv.DictWriter(f, fieldnames=field_names)
        csv_writer.writeheader()
        csv_writer.writerows(rows)


# ------------------------------------------------------------------------------
# Main orchestration
# ------------------------------------------------------------------------------
def main():
    # Acquire STS to identify own account first
    sts_client = boto3.client("sts")
    current_account = sts_client.get_caller_identity()["Account"]
    
    # Get list of all AWS regions
    regions = get_all_regions()

    if arole:
        # If role is provided, process for all accounts
        accounts = getallAccounts()
        logging.info(f'Accounts found --> {len(accounts)}')
        for act in accounts:
            if act == current_account or act == None:
                logging.info("Account number " + act)
            else:
                logging.info("Account number " + act)
                credentials = assume_role(act, arole)
                try:
                    for region in regions:
                        # Create EC2 client with assumed role
                        client = boto3.client('ec2',
                            region_name=region,
                            aws_access_key_id=credentials['AccessKeyId'], 
                            aws_secret_access_key=credentials['SecretAccessKey'], 
                            aws_session_token=credentials['SessionToken'])

                        getallvolumes(act, client, region)
                except Exception as e:
                    logging.info(f"Can't assume the role in account {act}: {e}")
                    continue
    else:
        # If role is not provided, scan for volumes in the current account directly
        for region in regions:
            client = boto3.client('ec2', region_name=region)
            getallvolumes(current_account, client, region)
    
    # After collecting all volumes, write them to CSV
    write_csv(file)


# ------------------------------------------------------------------------------
# Command-line entry point
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    # Define commandline arguments
    parser = argparse.ArgumentParser(description='Creates a CSV report about EBS volumes across all accounts and regions in your organization.')
    parser.add_argument('--file', required=True, help='Path for output CSV file')
    parser.add_argument('--role', required=False, help='IAM role that script can assume in other accounts')
    try:
        # Parse commandline arguments
        args = parser.parse_args()
        file = args.file
        arole = args.role
    except NameError:
        logging.error("Required arguments are missing. Please provide path for the file")

    # If CSV already exists, raise Exception
    if os.path.exists(file):
        raise Exception("File already exists!")
    else:
        main()
