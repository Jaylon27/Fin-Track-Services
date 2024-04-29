import azure.functions as func
import bcrypt

def main(req: func.HttpRequest, users: func.Out[func.SqlRow]) -> func.HttpResponse:

    # Extract JSON data from the HTTP request body
    req_body = req.get_json()

    # Extract specific fields from the request body
    username = req_body.get('username')       
    first_name = req_body.get('first_name')   
    last_name = req_body.get('last_name')     

    password = req_body.get('password').encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    # Convert the hashed password to a UTF-8 string before saving it
    hashed_password = hashed_password.decode('utf-8')

    
    if req_body:
        # Create a new user object
        new_user = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "password": hashed_password
        }

        # Save the new user to the database
        users.set(func.SqlRow.from_dict(new_user))

        # Return a success response
        return func.HttpResponse("User created successfully.", status_code=201)
    else:
        # Return an error response if username is not provided
        return func.HttpResponse("Please provide a username in the request body.", status_code=400)
