import os
import json
from datetime import datetime, timedelta
import io
import csv
import sys
import traceback
from typing import Dict

import boto3

TABLE_ARN = os.environ["TABLE_ARN"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
BOTS_BUCKET_NAME = os.environ.get("BOTS_BUCKET_NAME", "")
BOTS_METADATA_TABLE_ARN = os.environ.get("BOTS_METADATA_TABLE_ARN", "")

# Extract table name from ARN
def get_table_name_from_arn(arn: str) -> str:
    return arn.split('/')[-1]

dynamodb_client = boto3.client("dynamodb")
s3_client = boto3.client("s3")
dynamodb_resource = boto3.resource("dynamodb")


def process_metadata_item(item):
    """Processes a single item from BotsMetadataTable scan results,
    extracting relevant fields and denormalizing hierarchy data for Athena.
    """
    try:
        # --- DEBUG: Log the raw item structure (first 500 chars) ---
        # print(f"Processing raw item: {str(item)[:500]}") 

        # Use correct attribute names from BotsMetadataTable
        bot_id = item.get('bot_id')
        if not bot_id:
            print(f"Skipping item due to missing 'bot_id': {str(item)[:100]}")
            return None

        # --- DEBUG: Log extracted title and description ---
        extracted_title = item.get('title', '---TITLE_NOT_FOUND---')
        extracted_description = item.get('description', '---DESCRIPTION_NOT_FOUND---')
        print(f"BotID {bot_id}: Extracted Title='{extracted_title}', Description='{extracted_description}'")

        # Initialize bot_data dictionary for the Athena row
        bot_data = {
            'bot_id': bot_id,
            # Use the extracted values logged above
            'title': extracted_title if extracted_title != '---TITLE_NOT_FOUND---' else '', 
            'description': extracted_description if extracted_description != '---DESCRIPTION_NOT_FOUND---' else '',
            'owner_user_id': item.get('owner_user_id', ''), # Corrected field name
            'is_public': str(item.get('is_public', False)), # Convert boolean to string
            'create_time': str(item.get('create_time', '')), # Convert Decimal/Number to string
            'last_used_time': str(item.get('last_used_time', '')), # Convert Decimal/Number to string
            'is_deleted': str(item.get('is_deleted', False)), # Corrected field name & convert boolean
            'deleted_at': item.get('deleted_at', ''), # Should be ISO 8601 string or empty
            'updated_at': item.get('updated_at', '') # Should be ISO 8601 string or empty
        }

        # --- Denormalize Hierarchy --- 
        hierarchy_list = item.get('hierarchy', [])
        # Initialize hierarchy fields to empty strings
        bot_data['school_id'] = ''
        bot_data['school_name'] = ''
        bot_data['district_id'] = ''
        bot_data['district_name'] = ''
        bot_data['course_id'] = ''
        bot_data['course_name'] = ''
        
        if isinstance(hierarchy_list, list):
            for h_item in hierarchy_list:
                 # Check if h_item is a dictionary before accessing keys
                 if isinstance(h_item, dict):
                    level = h_item.get('level')
                    h_id = h_item.get('id', '')
                    h_name = h_item.get('name', '')
                    
                    if level == 'school':
                        bot_data['school_id'] = h_id
                        bot_data['school_name'] = h_name
                    elif level == 'district':
                        bot_data['district_id'] = h_id
                        bot_data['district_name'] = h_name
                    elif level == 'course':
                        bot_data['course_id'] = h_id
                        bot_data['course_name'] = h_name
                    # Add other levels if needed
                 else:
                     print(f"Warning: Unexpected item type in hierarchy list for bot {bot_id}: {type(h_item)}")
        else:
             print(f"Warning: Hierarchy field is not a list for bot {bot_id}: {type(hierarchy_list)}")

        # --- Denormalize Tags (Example - add if needed in Athena) --- 
        # tags_list = item.get('tags', [])
        # bot_data['tags_csv'] = ",".join([f"{t.get('category', '')}:{t.get('value', '')}" for t in tags_list if isinstance(t, dict)])
        
        # --- Denormalize Attributes (Example - add if needed in Athena) ---
        # attributes_list = item.get('attributes', [])
        # for attr in attributes_list:
        #      if isinstance(attr, dict) and attr.get('key'):
        #          bot_data[f"attr_{attr['key']}"] = attr.get('value', '') # Creates attr_KEY columns

        # Return bot_id and the processed bot_data dictionary
        return bot_id, bot_data

    except Exception as e:
        print(f"Error processing item: {str(item)[:200]}. Error: {str(e)}")
        traceback.print_exc()
        return None
        

# Simple wrapper for running async functions
def run_async_safely(coro):
    import asyncio
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return None  # Can't run in running loop without proper handling
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        return asyncio.run(coro)
    except Exception as e:
        print(f"Error running async function: {str(e)}")
        return {}


async def get_bots_from_metadata_table(table) -> Dict:
    """
    Get all bot records from the metadata table efficiently with pagination.
    Only include fields that exist in the database, no default values.
    
    Args:
        table: DynamoDB table object
        
    Returns:
        Dictionary mapping bot_id to bot record
    """
    bots = {}
    
    try:
        # Add debug logging for scan
        print(f"Starting scan of metadata table {table.name}")
        response = table.scan()
        
        # Log response structure
        print(f"Number of items returned: {len(response.get('Items', []))}")
        
        # Process initial items
        for item in response.get('Items', []):
            try:
                #print(f"Processing item: {type(item)}")
                result = process_metadata_item(item)
                if result:
                    bot_id, bot_data = result
                    bots[bot_id] = bot_data
            except Exception as e:
                print(f"Error processing item in metadata table: {str(e)}")
                print(f"Stack trace: {traceback.format_exc()}")
                print(f"Problematic item: {str(item)[:200]}")
                continue
        
        # Handle pagination with same error logging
        while 'LastEvaluatedKey' in response:
            try:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                print(f"Pagination scan returned {len(response.get('Items', []))} items")
                
                for item in response.get('Items', []):
                    try:
                        result = process_metadata_item(item)
                        if result:
                            bot_id, bot_data = result
                            bots[bot_id] = bot_data
                    except Exception as e:
                        print(f"Error processing item in pagination: {str(e)}")
                        print(f"Stack trace: {traceback.format_exc()}")
                        print(f"Problematic item: {str(item)[:200]}")
                        continue
            except Exception as e:
                print(f"Error during pagination: {str(e)}")
                print(f"Stack trace: {traceback.format_exc()}")
                break
        
        print(f"Found {len(bots)} valid bot records in metadata table")
        return bots
        
    except Exception as e:
        print(f"Error scanning metadata table: {str(e)}")
        print(f"Stack trace: {traceback.format_exc()}")
        raise

def export_conversation_ddb_to_s3(execution_time):
    """Export the dynamodb table to S3 for the last hour to analyze the usage for admin."""
    last_hour = (execution_time - timedelta(hours=1)).replace(
        minute=0, second=0, microsecond=0
    )
    current_hour = execution_time.replace(minute=0, second=0, microsecond=0)

    s3_prefix = current_hour.strftime("%Y/%m/%d/%H")

    print(f"TABLE_ARN: {TABLE_ARN}")
    print(f"BUCKET_NAME: {BUCKET_NAME}")
    print(f"last_hour: {last_hour}")
    print(f"current_hour: {current_hour}")
    print(f"s3_prefix: {s3_prefix}")

    response = dynamodb_client.export_table_to_point_in_time(
        TableArn=TABLE_ARN,
        S3Bucket=BUCKET_NAME,
        S3Prefix=s3_prefix,
        ExportType="INCREMENTAL_EXPORT",
        IncrementalExportSpecification={
            # NOTE: The export period's start time is inclusive and the end time is exclusive.
            # Ref: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/S3DataExport_Requesting.html#S3DataExport_Requesting_Console
            "ExportFromTime": last_hour,
            "ExportToTime": current_hour,
            "ExportViewType": "NEW_AND_OLD_IMAGES",
        },
    )
    
    return response


def export_bots_to_s3():
    """Export bot data to S3 for Athena analytics."""
    if not BOTS_BUCKET_NAME:
        print("BOTS_BUCKET_NAME not set, skipping bot export")
        return None
        
    if not BOTS_METADATA_TABLE_ARN:
        print("BOTS_METADATA_TABLE_ARN not set, skipping bot export")
        return None
        
    print(f"Exporting bots data to S3 bucket: {BOTS_BUCKET_NAME}")
    
    # Get bot data exclusively from the metadata table
    try:
        metadata_table_name = get_table_name_from_arn(BOTS_METADATA_TABLE_ARN)
        print(f"Using metadata table: {metadata_table_name} ({BOTS_METADATA_TABLE_ARN})")
        
        metadata_table = dynamodb_resource.Table(metadata_table_name)
        print(f"Attempting to scan {metadata_table_name} table")
        
        # Use the imported function to get bots
        metadata_bots = run_async_safely(get_bots_from_metadata_table(metadata_table))
        metadata_bot_items = list(metadata_bots.values()) if metadata_bots else []
        
        print(f"Found {len(metadata_bot_items)} bots in metadata table")
        
        if not metadata_bot_items:
            print("No bot items found in metadata table, skipping export")
            return None
        
        # Create CSV for Athena
        csv_buffer = io.StringIO()
        
        # --- EDIT: Define fixed fieldnames matching the Glue table schema ---
        fieldnames = [
            'bot_id', 'course_id', 'course_name', 'create_time', 'deleted_at', 
            'description', 'district_id', 'district_name', 'is_deleted', 
            'is_public', 'last_used_time', 'owner_user_id', 'school_id', 
            'school_name', 'title', 'updated_at'
        ]
        # --- End Edit ---
        
        writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
        writer.writeheader()
        
        # Write all bots, ensuring default values for missing fields
        for bot in metadata_bot_items:
            # Ensure all fields in the fixed list exist with empty defaults
            row_to_write = {}
            for field in fieldnames:
                 row_to_write[field] = bot.get(field, '') # Use .get() for safety
            writer.writerow(row_to_write) # Write the filtered/defaulted row
        
        # Convert to bytes for S3
        csv_bytes = csv_buffer.getvalue().encode('utf-8')
        
        # Upload to S3
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        key = f"bots_analytics/bots_export_{timestamp}.csv"
        
        try:
            s3_client.put_object(
                Bucket=BOTS_BUCKET_NAME,
                Key=key,
                Body=csv_bytes
            )
            
            print(f"Uploaded bot data to s3://{BOTS_BUCKET_NAME}/{key}")
            return key
        except Exception as s3_err:
            print(f"Error uploading to S3: {str(s3_err)}")
            return None
            
    except Exception as meta_err:
        print(f"Error accessing metadata table: {str(meta_err)}")
        print(traceback.format_exc())
        return None


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def convert_datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: convert_datetime_to_string(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime_to_string(item) for item in obj]
    return obj


def handler(event, context):
    """Lambda handler that exports both DynamoDB data and bot data."""
    print(event)
    
    execution_time = datetime.strptime(event["time"], "%Y-%m-%dT%H:%M:%SZ")
    
    # Export DynamoDB data
    ddb_response = export_conversation_ddb_to_s3(execution_time)
    
    # Convert all datetime objects in the DynamoDB response to ISO format strings
    if ddb_response:
        ddb_response = convert_datetime_to_string(ddb_response)
    
    # Export bot data
    bot_response = export_bots_to_s3()
    
    # Then use it to debug:
    print("DDB Response:", json.dumps(ddb_response, cls=DateTimeEncoder))
    
    return {
        "ddb_export": ddb_response,
        "bot_export": bot_response if bot_response else "No bot data to export"
    }
