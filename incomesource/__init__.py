import os
import jwt
from datetime import datetime
import azure.functions as func

def format_amount(amount):
    # Format balance as dollar amount
    return '${:,.2f}'.format(amount)

def main(req: func.HttpRequest, income: func.Out[func.SqlRow]) -> func.HttpResponse:

    # Extract JSON data from the request body
    req_body = req.get_json()

    # Extract required fields from the request body
    source = req_body.get('source')
    amount = req_body.get('amount')
    date = req_body.get('date')

    # Extract authorization token from the request headers
    auth_header = req.headers.get('Authorization')
    if not auth_header:
        return func.HttpResponse("Authorization header is missing", status_code=400)

    # Extract token from the authorization header
    token = auth_header.split('Bearer ')[-1]

    try:
        # Verify and decode JWT token
        jwt_secret = os.environ.get('jwt_secret')   
        decoded_token = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
    
    except jwt.ExpiredSignatureError:
        return func.HttpResponse("Token has expired", status_code=401)
    except jwt.InvalidTokenError:
        return func.HttpResponse("Invalid token", status_code=401)
    except Exception as e:
        return func.HttpResponse(f"Error decoding token: {str(e)}", status_code=500)

    if req_body:
        # Create a new income object
        new_income = {
            "source": source,
            "amount": format_amount(amount),
            "date": datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d'),
            "user_id": user_id
        }

        # Store the new income object in the database
        income.set(func.SqlRow.from_dict(new_income))

        # Return a success response
        return func.HttpResponse(f"Source of income added successfully.", status_code=201)
    else:
        # Return an error response if income data is not provided
        return func.HttpResponse("Please provide income data in the request body.", status_code=400)
