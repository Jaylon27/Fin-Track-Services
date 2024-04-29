import os
import jwt
import azure.functions as func

def format_balance(balance):
    # Format balance as dollar amount
    return '${:,.2f}'.format(balance)

def main(req: func.HttpRequest, accounts: func.Out[func.SqlRow]) -> func.HttpResponse:

    # Extract JSON data from the HTTP request body
    req_body = req.get_json()

    # Extract specific fields from the request body
    name = req_body.get('name')
    type = req_body.get('type')
    balance = req_body.get('balance')

    # Extract authorization token from the request headers
    auth_header = req.headers.get('Authorization')
    if not auth_header:
        # Return a 400 status code if Authorization header is missing
        return func.HttpResponse("Authorization header is missing", status_code=400)

     # Extract token from the authorization header
    token = auth_header.split('Bearer ')[-1]

    try:
        # Verify and decode JWT token
        jwt_secret = os.environ.get('jwt_secret')   
        decoded_token = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')
    except jwt.ExpiredSignatureError:
        # Return a 401 status code if the token has expired
        return func.HttpResponse("Token has expired", status_code=401)
    except jwt.InvalidTokenError:
        # Return a 401 status code if the token is invalid
        return func.HttpResponse("Invalid token", status_code=401)
    except Exception as e:
        # Return a 500 status code if there's an error decoding the token
        return func.HttpResponse(f"Error decoding token: {str(e)}", status_code=500)

    if req_body:
        # Create a new account object
        new_account = {
            "name": name,
            "type": type,
            "balance": format_balance(balance),
            "user_id": user_id
        }

        # Save the new accunt to the database
        accounts.set(func.SqlRow.from_dict(new_account))

        # Return a success response
        return func.HttpResponse(f"Account added successfully.", status_code=201)
    else:
        # Return a 400 status code if account details are missing from the request body
        return func.HttpResponse("Please provide an account in the request body.", status_code=400)
