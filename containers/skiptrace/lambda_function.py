from utils import json_to_database, skiptrace_leads

# Lambda function entry point
def handler(event, context):
    try:
        skiptrace_leads()
        json_to_database()

        return {
            'statusCode': 200,
            'body': 'Data skiptraced successfully.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'An error occurred: {str(e)}'
        }