import logging
import json
import hashlib
import azure.functions as func


# def get_users(users: func.Out[func.SqlRow]) -> list:
#     sql_rows = users.execute()
#     rows = []
#     for row in sql_rows:
#         rows.append(json.loads(row.to_json()))
#     return rows



# def create_user(user_data: dict, users: func.Out[func.SqlRow]) -> None:
#     # Hash the password before storing it in the database
#     hashed_password = hashlib.sha256(user_data['password'].encode()).hexdigest()
    
#     # Construct a new user row
#     new_user = {
#         'username': user_data['username'],
#         'password': hashed_password,
#         'first_name': user_data.get('first_name', ''),
#         'last_name': user_data.get('last_name', '')
#     }

#     # Save the new user to the database
#     users.set(func.SqlRow.from_dict(new_user))

# def main(req: func.HttpRequest, users: func.Out[func.SqlRow]) -> func.HttpResponse:
#     if req.method == 'POST':
#         req_body = req.get_json()
#         if not req_body or 'username' not in req_body or 'password' not in req_body:
#             return func.HttpResponse("Invalid request body", status_code=400)

#         create_user(req_body, users)
        
#         return func.HttpResponse("User account created successfully", status_code=201)
    
#     elif req.method == 'GET':
#         # Handle GET request
#         rows = get_users(users)
#         return func.HttpResponse(
#             json.dumps(rows),
#             status_code=200,
#             mimetype="application/json"
#         )

#     else:
#         return func.HttpResponse("Method not allowed", status_code=405)

def main(req: func.HttpRequest, users: func.SqlRowList) -> func.HttpResponse:
    rows = list(map(lambda r: json.loads(r.to_json()), users))

    return func.HttpResponse(
        json.dumps(rows),
        status_code=200,
        mimetype="application/json"
    ) 