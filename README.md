# Enigma recruitment task
This Django project, created for a recruitment task, serves as a REST API simulating an e-commerce application. It provides various endpoints for displaying product lists, placing orders, and more.

## Prerequisites
Before you begin, ensure you have met the following requirements:
- Python 3.x installed on your system.
- Python Virtual Environment (venv)
- SQLite 3

## Technology Stack
- Django 5.0.1
- Django Rest Framework 3.14.0
- SQLite 3

## Getting Started
1. Clone the repository:
```
git clone https://github.com/barxtex1/Enigma-task-API.git
cd Enigma-task-API
```
2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate
venv\Scripts\activate (for Windows users)
```
3. Install the required packages:
```
pip install -r requirements.txt
```
4. Go to the project directory and run migrations:
```
python manage.py makemigrations
python manage.py migrate
```
5. Run server in your local network:
```
python manage.py runserver
```
The project will now be running at [localhost](http://localhost:8000/)

## Usage
### Authentication
To interact with the API, you need to obtain an authentication token. You can use the administration panel with credentials `admin:admin` or use the `/api/token/` endpoint with a POST request, providing the username and password:
```
curl -X POST -d "username=user_username&password=user_password" http://localhost:8000/api/token/
```
All access data is available on file: `tests/credentials.json`
The authentication token will be used to access protected endpoints.

### Endpoints
- Admin Panel:
    - Access at http://localhost:8000/admin/
    - Credentials: admin:admin
- Product List:
    - Endpoint: http://localhost:8000/api/product/
    - Method: GET (for all users, even not authenticated)
    - Methods: POST, PUT, DELETE (for **vendors** users)
- Product Details:
    - Endpoint: [`http://localhost:8000/api/product/<int:pk>/`](http://localhost:8000/api/product/<int:pk>/)
    - Method: GET (for all users, even not authenticated)
- Order Placement:
    - Endpoint: http://localhost:8000/api/order/
    - Method: POST (for **customers** users)
- Order Statistics (most frequently ordered products):
    - Endpoint: http://localhost:8000/api/order/statistics/most-ordered/
    - Method: GET (for **vendors** users)

## Running Tests
Tests have been written for this project and can be executed using the following command:
```
python manage.py test --keepdb
```