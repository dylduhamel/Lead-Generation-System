from utils import remove_duplicates
import sys
# Ensure your Lambda deployment package includes dependencies
sys.path.append('..')


def handler(event, context):
    try:
        # Call your function
        remove_duplicates()
        # Log and return a success message
        return {
            'statusCode': 200,
            'body': 'Duplicates removed successfully'
        }
    except Exception as e:
        # Return an error response
        return {
            'statusCode': 500,
            'body': f'An error occurred: {str(e)}'
        }
