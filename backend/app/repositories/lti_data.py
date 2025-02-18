import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('LTI_DATA_TABLE_NAME', 'LtiDataTablexxx')  # Get table name from environment variable
table = dynamodb.Table(table_name)

def add_lti_data(lti_id: str, client_id: str):
    try:
        response = table.put_item(
            Item={
                'lti_id': lti_id,
                'client_id': client_id
            }
        )
        return response
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None

def get_lti_data(lti_id: str):
    print('table name = ', table_name)
    print('Getting LTI data for:', lti_id)
    try:
        response = table.get_item(
            Key={
                'lti_id': lti_id
            }
        )
        return response.get('Item')
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None

def delete_lti_data(lti_id: str):
    try:
        response = table.delete_item(
            Key={
                'lti_id': lti_id
            }
        )
        return response
    except ClientError as e:
        print(e.response['Error']['Message'])
        return None
