import os
import jwt
from datetime import datetime
import azure.functions as func

def format_amount(amount):
    # Format amount as dollar amount
    return '${:,.2f}'.format(amount)

def main(req: func.HttpRequest, savingsgoals: func.Out[func.SqlRow]) -> func.HttpResponse:
    # Parse request body
    req_body = req.get_json()

    # Extract data from request body
    name = req_body.get('name')
    amount = req_body.get('amount')
    duedate = req_body.get('duedate')
    status = req_body.get('status')

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
        # Create a new savings goal object
        new_savings_goal = {
            "name": name,
            "amount": format_amount(amount),
            "duedate": datetime.strptime(duedate, '%Y-%m-%d').strftime('%Y-%m-%d'),
            "status": status,
            "user_id": user_id
        }

        # Save the new savings goal to the database
        savingsgoals.set(func.SqlRow.from_dict(new_savings_goal))

        # Return a success response
        return func.HttpResponse(f"Savings goal added successfully.", status_code=201)
    else:
        # Return an error response if request body is empty
        return func.HttpResponse("Please provide a savings goal in the request body.", status_code=400)

