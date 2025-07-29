import json
import logging

# AWS Lambda Function Logging in Python
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    '''Demonstrates Amazon API Gateway Lambda proxy integration. You have full
    access to the request and response payload, including headers and
    status code.
    
    '''
    logger.debug(event) # Mind logger.setLevel at line 6. Check Event printed at CloudWatch

    #/pets/{petId}
    pets = [
        { "id": "1", "name": "Peach"},
        { "id": "2", "name": "Chuck"},
        { "id": "3", "name": "Lelow"}
    ]
    
    
    # Input Format 
    resource = event['resource']
    # Uncomment to print the event
    # print("Received event: " + json.dumps(event, indent=2))

    err = None
    # /pets List all pets
    response_body = {}
    if (resource == "/pets"):
        response_body = {
            "pets": pets
        }
    # /pets/petId find pet by Id    
    elif (resource == "/pets/{id}"):
        petId = event['pathParameters']['id']
        value = next((item for item in pets if item["id"] == str(petId)), False)
        if( value == False ):
            err = "Pet not found"
        else:
            response_body = {
                "pet": value
            }

        
    response =  response_payload(err, response_body)

    return response
  
  
    
'''
In Lambda proxy integration, API Gateway sends the entire request as input to a backend Lambda function. 
API Gateway then transforms the Lambda function output to a frontend HTTP response.

'''
def response_payload(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }
