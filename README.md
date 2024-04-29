# Financial Management API

The Financial Management API is a serverless solution designed to manage users' financial data securely. It provides functionalities for user registration, authentication, and management of financial assets such as income, expenses, savings goals, credit cards, and accounts.

# Technologies Used
Azure Functions: Leveraging serverless compute to handle HTTP requests and execute business logic.
Azure SQL Database: Storing and managing user data securely.
Python: Backend programming language used for implementing the API logic.
Bcrypt: Hashing user passwords to ensure secure storage.
JSON Web Tokens (JWT): Implementing user authentication and authorization.

# Key Features
User Registration: Allows users to register accounts by providing basic information such as username, first name, last name, and password. Passwords are securely hashed using bcrypt before storing in the database.
User Authentication: Implements JWT-based authentication to verify user identity and authorize access to protected endpoints.
Financial Data Management: Enables users to manage various financial aspects including income sources, expenses, savings goals, credit cards, and accounts.
Secure Data Storage: Utilizes Azure SQL Database to store user data in a secure and scalable manner.
Serverless Architecture: Built using Azure Functions, ensuring cost-effectiveness, scalability, and high availability.

# Security
Password Hashing: User passwords are hashed using bcrypt before storing in the database, ensuring that plaintext passwords are never stored.
JWT-based Authentication: Implements JWT tokens for user authentication, preventing unauthorized access to protected endpoints.
Authorization Checks: Performs authorization checks to ensure that users can only access their own financial data.

# Usage
User Registration: Send a POST request to /api/register with the required user information in the request body.
User Login: Send a POST request to /api/login with the username and password in the request body to obtain a JWT token.
Access Protected Endpoints: Include the JWT token in the Authorization header of subsequent requests to access protected endpoints.
Manage Financial Data: Use the API endpoints for managing income sources, expenses, savings goals, credit cards, and accounts.
