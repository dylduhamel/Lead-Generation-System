from utils import email_csv

# Lambda function entry point
def handler(event, context):
    try:
        email_csv()

        return {
            'statusCode': 200,
            'body': 'Data emailed successfully.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'An error occurred: {str(e)}'
        }