import boto3
import botocore
import json
from datetime import datetime

s3 = boto3.client('s3')

def lambda_handler(event, context):
	bucket_name = 'your_bucket_name'
	now = datetime.now()
	file_key = 'log_' + str(now)[:10] + '.json'
	event_json = json.loads(event['body'])

	try:
		s3.head_object(Bucket=bucket_name, Key=file_key)
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "404":
			create_json_file(bucket_name, file_key, event_json)
			return {
				'statusCode': 200,
				'body': json.dumps('File uploaded successfully.')
			}
		else:
			return {
				'statusCode': 400,
				'body': json.dumps('Something went wrong.')
			}

	update_json_file(bucket_name, file_key, event_json)
	return {
		'statusCode': 200,
		'body': json.dumps('File updated successfully.')
	}

def create_json_file(bucket_name, file_key, new_object):
	array = []
	array.append(new_object)
	json_array = json.dumps(array)
	s3.put_object(Body=json_array, Bucket=bucket_name, Key=file_key)

def update_json_file(bucket_name, file_key, new_object):
	response = s3.get_object(Bucket=bucket_name, Key=file_key)
	json_content = response['Body'].read().decode('utf-8')
	data = json.loads(json_content)
	data.append(new_object)
	updated_json_content = json.dumps(data)
	s3.put_object(Body=updated_json_content, Bucket=bucket_name, Key=file_key)
