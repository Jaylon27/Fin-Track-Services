import json
import os
import bcrypt
import jwt
import datetime 
import azure.functions as func

def main(req: func.HttpRequest, users: func.SqlRowList) -> func.HttpResponse:
    # Convert SqlRowList to list of dictionaries
    rows = list(map(lambda r: json.loads(r.to_json()), users))

    user_found = False
    password_correct = False
    user_id = None

    # Parse request body
    req_body = req.get_json()

    # Extract username and password from request body
    username = req_body.get('username')
    password = req_body.get('password').encode('utf-8')

    # Check each user in the database
    for row in rows:
        getusername = row.get('username')
        getpassword = row.get('password')

        # Check if username matches
        if getusername == username:
            user_found = True

            # Check if password matches
            if bcrypt.checkpw(password, getpassword.encode('utf-8')):
                password_correct = True
                user_id = row.get('id')
                first_name = row.get('first_name')
                last_name = row.get('last_name')
                break  # Exit loop if username matches and password is correct
            else:
                break  # Exit loop if username matches but password is incorrect

    # Return appropriate HTTP response based on login result
    if user_found and password_correct:
        # Generate JWT token
        token_payload = {'user_id': user_id, 'username': username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}  
        jwt_secret = os.environ.get('jwt_secret')
        jwt_token = jwt.encode(token_payload, jwt_secret, algorithm='HS256')

        # Construct response data
        response_data = {
            'userId': user_id,
            'firstName': first_name,
            'lastName': last_name,
            'sessionToken': jwt_token
        }

        response_json = json.dumps(response_data)

        return func.HttpResponse(response_json, status_code=200, mimetype="application/json")
    else:
        # Return error response if username or password is incorrect
        return func.HttpResponse("Invalid username or password", status_code=401)
