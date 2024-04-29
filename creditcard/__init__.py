import os
import jwt
from datetime import datetime
import azure.functions as func

def format_balance(balance):
    # Format balance as dollar amount
    return '${:,.2f}'.format(balance)

def main(req: func.HttpRequest, creditcards: func.Out[func.SqlRow]) -> func.HttpResponse:
    
    # Parse request body
    req_body = req.get_json()

    # Extract data from request body
    cardname = req_body.get('cardname')
    balance = req_body.get('balance')
    duedate = req_body.get('duedate')

    # Check for Authorization header
    auth_header = req.headers.get('Authorization')
    if not auth_header:
        # Return error response if Authorization header is missing
        return func.HttpResponse("Authorization header is missing", status_code=400)

    # Extract token from Authorization header
    token = auth_header.split('Bearer ')[-1]

    try:
        # Verify and decode JWT token
        jwt_secret = os.environ.get('jwt_secret')
        decoded_token = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')

    except jwt.ExpiredSignatureError:
        # Return error response if token has expired
        return func.HttpResponse("Token has expired", status_code=401)
    except jwt.InvalidTokenError:
        # Return error response if token is invalid
        return func.HttpResponse("Invalid token", status_code=401)
    except Exception as e:
        # Return error response for other exceptions
        return func.HttpResponse(f"Error decoding token: {str(e)}", status_code=500)

    if req_body:
         # Create a new credit card object
        new_creditcard = {
            "cardname": cardname,
            "balance": format_balance(balance),
            "duedate": datetime.strptime(duedate, '%Y-%m-%d').strftime('%Y-%m-%d'),
            "user_id": user_id
        }

        # Add new credit card to the database
        creditcards.set(func.SqlRow.from_dict(new_creditcard))

        # Return a success response
        return func.HttpResponse(f"Credit card added successfully.", status_code=201)
    else:
        # Return an error response if request body is empty
        return func.HttpResponse("Please provide a credit card in the request body.", status_code=400)
