import json
import jwt
import azure.functions as func

def main(req: func.HttpRequest, income: func.SqlRowList) -> func.HttpResponse:
    # Convert SqlRowList to list of dictionaries
    rows = list(map(lambda r: json.loads(r.to_json()), income))

    # Check for Authorization header
    auth_header = req.headers.get('Authorization')
    if not auth_header:
        # Return error response if Authorization header is missing
        return func.HttpResponse("Authorization header is missing", status_code=400)

    try:
        # Extract 'id' from request parameters
        id = req.params.get('id')

        if not id:
            # Return error response if 'id' is missing in the request parameters
            return func.HttpResponse("ID is missing in the request parameters", status_code=400)
        
        # Check if any row in the income matches the provided 'id'
        if any(row.get('id') == id for row in rows):
            # Return error response if 'id' exists in income
            return func.HttpResponse("Failed to delete income source.", status_code=500)
        else:
            # Return success response if 'id' does not exist in income
            return func.HttpResponse("Income source deleted successfully", status_code=200)
        
    except jwt.ExpiredSignatureError:
        # Return error response if token has expired
        return func.HttpResponse("Token has expired", status_code=401)
    except jwt.InvalidTokenError:
        # Return error response if token is invalid
        return func.HttpResponse("Invalid token", status_code=401)
    except Exception as e:
        # Return error response for other exceptions
        return func.HttpResponse(f"Error decoding token: {str(e)}", status_code=500)
