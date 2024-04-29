import os
import json
import jwt
from datetime import datetime
import azure.functions as func

def format_amount(amount):
    # Format balance as dollar amount
    return '${:,.2f}'.format(amount)


def main(req: func.HttpRequest, income: func.SqlRowList) -> func.HttpResponse:
    # Convert SqlRowList to list of dictionaries
    rows = list(map(lambda r: json.loads(r.to_json()), income))

    # Extract authorization token from the request headers
    auth_header = req.headers.get('Authorization')
    if not auth_header:
        # Return error response if Authorization header is missing
        return func.HttpResponse("Authorization header is missing", status_code=400)

    # Extract token from the authorization header
    token = auth_header.split('Bearer ')[-1]

    try:
        # Verify and decode JWT token
        jwt_secret = os.environ.get('jwt_secret')
        decoded_token = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        user_id = decoded_token.get('user_id')

        # Filter user data based on user_id
        user_data = [row for row in rows if row.get('user_id') == user_id]

        for data in user_data:
            if 'date' in data:
                # Convert date format if 'date' field exists
                data['date'] = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')

            if 'amount' in data:
                # Format 'amount' field as dollar amount
                data['amount'] = format_amount(data['amount'])

        # Return filtered and formatted user data
        return func.HttpResponse(json.dumps(user_data), status_code=200, mimetype="application/json")
    
    except jwt.ExpiredSignatureError:
        # Return error response if token has expired
        return func.HttpResponse("Token has expired", status_code=401)
    except jwt.InvalidTokenError:
        # Return error response if token is invalid
        return func.HttpResponse("Invalid token", status_code=401)
    except Exception as e:
        # Return error response for other exceptions
        return func.HttpResponse(f"Error decoding token: {str(e)}", status_code=500)



