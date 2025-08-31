# TamuCuts API Testing Guide

This guide provides instructions for testing the TamuCuts API endpoints for a 5-minute demo video. It covers authentication, user and product creation, order processing with stock deduction, daily reporting, and product CRUD operations. Each endpoint includes the URL, request type, JSON body (aligned with the `butchery` app models), expected response, response types, and notes on functionality and side effects. The API is built with Django REST Framework and uses JWT authentication. To avoid JSON parse errors, copy-paste the provided JSON bodies exactly.

## Prerequisites
- **Server**: Run `python manage.py runserver` (default: `http://localhost:8000`).
- **Database**: Fresh SQLite (`db.sqlite3`). Reset with `rm db.sqlite3 && python manage.py makemigrations && python manage.py migrate`.
- **Superuser**: Username: `Marto`, Password: `pass123`, Role: `admin` (create via `python manage.py createsuperuser`).
- **Tools**: Postman or Thunder Client (VS Code). Set environment variables:
  - `base_url`: `http://localhost:8000/api`
  - `auth_token`: (set after authentication)
- **Date**: August 31, 2025 (for report consistency).

## Testing Flow
1. Authenticate to obtain a JWT token.
2. Create a customer user.
3. Create a product.
4. Create an order and order item.
5. Verify stock transaction and deduction.
6. Generate a daily report.
7. Perform product CRUD operations (update and delete).

## API Endpoints

### 1. Authenticate (Get JWT Token)
- **URL**: `{{base_url}}/token/`
- **Method**: POST
- **Headers**: `Content-Type: application/json`
- **Body**:
  ```json
  {
    "username": "Marto",
    "password": "pass123"
  }
  ```
- **Expected Response**: 200 OK
  ```json
  {
    "access": "<access_token>",
    "refresh": "<refresh_token>"
  }
  ```
- **Response Types**:
  - **200 OK**: Successful authentication, returns access and refresh tokens.
  - **400 Bad Request**: Invalid username or password.
- **Notes**: Authenticates the admin user `Marto` to obtain a JWT token for subsequent requests. Set `access` token as `auth_token` for use in `Authorization: Bearer {{auth_token}}` headers.

### 2. Create Customer User
- **URL**: `{{base_url}}/users/`
- **Method**: POST
- **Headers**: `Authorization: Bearer {{auth_token}}`, `Content-Type: application/json`
- **Body**:
  ```json
  {
    "username": "customer1",
    "email": "customer1@tamucuts.com",
    "password": "pass123",
    "role": "customer",
    "phone_number": "+254712345678"
  }
  ```
- **Expected Response**: 201 Created
  ```json
  {
    "id": 2,
    "username": "customer1",
    "email": "customer1@tamucuts.com",
    "role": "customer",
    "phone_number": "+254712345678",
    "is_staff": false,
    "is_active": true
  }
  ```
- **Response Types**:
  - **201 Created**: User created successfully.
  - **400 Bad Request**: Invalid data (e.g., duplicate username, invalid email).
  - **403 Forbidden**: User lacks admin role.
- **Notes**: Creates a customer user for placing orders. Requires `role=admin` for the authenticated user. Verify the user in `/admin/butchery/user/`.

### 3. Create Product
- **URL**: `{{base_url}}/products/`
- **Method**: POST
- **Headers**: `Authorization: Bearer {{auth_token}}`, `Content-Type: application/json`
- **Body**:
  ```json
  {
    "name": "Beef Sirloin",
    "category": "beef",
    "price": 12.50,
    "stock_quantity": 100
  }
  ```
- **Expected Response**: 201 Created
  ```json
  {
    "id": 1,
    "name": "Beef Sirloin",
    "category": "beef",
    "price": "12.50",
    "stock_quantity": 100,
    "created_at": "2025-08-31T20:50:00Z",
    "updated_at": "2025-08-31T20:50:00Z"
  }
  ```
- **Response Types**:
  - **201 Created**: Product created successfully.
  - **400 Bad Request**: Invalid data (e.g., negative price or stock).
  - **403 Forbidden**: User lacks admin role.
- **Notes**: Adds a product to the inventory. Requires `role=admin`. Used for order items and stock management.

### 4. Create Order
- **URL**: `{{base_url}}/orders/`
- **Method**: POST
- **Headers**: `Authorization: Bearer {{auth_token}}`, `Content-Type: application/json`
- **Body**:
  ```json
  {
    "customer_id": 2,
    "status": "PENDING",
    "payment_type": "CASH"
  }
  ```
- **Expected Response**: 201 Created
  ```json
  {
    "id": 1,
    "customer": {
      "id": 2,
      "username": "customer1",
      "email": "customer1@tamucuts.com",
      "role": "customer",
      "phone_number": "+254712345678",
      "is_staff": false,
      "is_active": true
    },
    "status": "PENDING",
    "payment_type": "CASH",
    "created_at": "2025-08-31T20:51:00Z",
    "updated_at": "2025-08-31T20:51:00Z",
    "items": []
  }
  ```
- **Response Types**:
  - **201 Created**: Order created successfully.
  - **400 Bad Request**: Invalid `customer_id` or choices (e.g., `status` not in ["PENDING", "PROCESSING", "COMPLETED", "CANCELLED"]).
  - **401 Unauthorized**: Missing or invalid token.
- **Notes**: Creates an order for a customer. Any authenticated user can perform this action. Used to group order items.

### 5. Create Order Item
- **URL**: `{{base_url}}/order-items/`
- **Method**: POST
- **Headers**: `Authorization: Bearer {{auth_token}}`, `Content-Type: application/json`
- **Body**:
  ```json
  {
    "order": 1,
    "product_id": 1,
    "quantity": 5
  }
  ```
- **Expected Response**: 201 Created
  ```json
  {
    "id": 1,
    "order": 1,
    "product": {
      "id": 1,
      "name": "Beef Sirloin",
      "category": "beef",
      "price": "12.50",
      "stock_quantity": 95,
    
    },
    "quantity": 5,
    "total_price": "62.50"
  }
  ```
- **Response Types**:
  - **201 Created**: Order item created, stock deducted, transaction logged.
  - **400 Bad Request**: Invalid `order` or `product_id`, or insufficient stock.
  - **401 Unauthorized**: Missing or invalid token.
- **Notes**: Adds an item to an order, deducts `quantity` from product stock, and logs a `StockTransaction` (`type="OUT"`). Any authenticated user can perform this action.

### 6. Verify Stock Transaction
- **URL**: `{{base_url}}/products/1/`
- **Method**: GET
- **Headers**: `Authorization: Bearer {{auth_token}}`
- **Body**: None
- **Expected Response**: 200 OK
  ```json
  {
    "id": 1,
    "name": "Beef Sirloin",
    "category": "beef",
    "price": "12.50",
    "stock_quantity": 95,
    ...
  }
  ```
- **Second Request**: Check transaction
  - **URL**: `{{base_url}}/stock-transactions/`
  - **Method**: GET
  - **Headers**: `Authorization: Bearer {{auth_token}}`
  - **Expected Response**: 200 OK
    ```json
    [
      {
        "id": 1,
        "product": 1,
        "transaction_type": "OUT",
        "quantity": 5,
        "date": "2025-08-31",
        "remarks": "Order item sale",
        ...
      }
    ]
    ```
- **Response Types**:
  - **200 OK**: Returns product or transaction list.
  - **401 Unauthorized**: Missing or invalid token.
  - **404 Not Found**: Invalid `product_id`.
- **Notes**: Verifies stock reduction (from 100 to 95) and transaction log after order item creation. Any authenticated user can view these.

### 7. Get Daily Report
- **URL**: `{{base_url}}/reports/2025-08-31/`
- **Method**: GET
- **Headers**: `Authorization: Bearer {{auth_token}}`
- **Body**: None
- **Expected Response**: 200 OK
  ```json
  {
    "date": "2025-08-31",
    "opening_stock": 0,
    "sales": 5,
    "closing_stock": 0,
    "revenue": "62.50"
  }
  ```
- **Response Types**:
  - **200 OK**: Returns aggregated report.
  - **403 Forbidden**: User lacks admin role.
  - **401 Unauthorized**: Missing or invalid token.
- **Notes**: Generates a daily report with stock and revenue aggregates for the specified date. Requires `role=admin`.

### 8. Product CRUD (Update & Delete)
- **Update (PATCH)**:
  - **URL**: `{{base_url}}/products/1/`
  - **Method**: PATCH
  - **Headers**: `Authorization: Bearer {{auth_token}}`, `Content-Type: application/json`
  - **Body**:
    ```json
    {
      "price": 13.00
    }
    ```
  - **Expected Response**: 200 OK
    ```json
    {
      "id": 1,
      "name": "Beef Sirloin",
      "category": "beef",
      "price": "13.00",
      "stock_quantity": 95,
      ...
    }
    ```
  - **Response Types**:
    - **200 OK**: Product updated successfully.
    - **400 Bad Request**: Invalid data (e.g., negative price).
    - **403 Forbidden**: User lacks admin role.
    - **404 Not Found**: Invalid `product_id`.
- **Delete**:
  - **URL**: `{{base_url}}/products/1/`
  - **Method**: DELETE
  - **Headers**: `Authorization: Bearer {{auth_token}}`
  - **Body**: None
  - **Expected Response**: 204 No Content
  - **Response Types**:
    - **204 No Content**: Product deleted successfully.
    - **403 Forbidden**: User lacks admin role.
    - **404 Not Found**: Invalid `product_id`.
- **Verify Deletion**:
  - **URL**: `{{base_url}}/products/`
  - **Method**: GET
  - **Headers**: `Authorization: Bearer {{auth_token}}`
  - **Expected Response**: 200 OK, `[]` (empty list if no other products).
  - **Response Types**:
    - **200 OK**: Returns product list.
    - **401 Unauthorized**: Missing or invalid token.
- **Notes**: Updates the product price and deletes the product. Both actions require `role=admin`. Verify deletion with GET request.

## Troubleshooting
- **401 Unauthorized**: Invalid or expired token. Refresh via `{{base_url}}/token/refresh/`.
- **403 Forbidden**: Ensure `Marto` has `role=admin` (check `/admin/butchery/user/`).
- **400 Bad Request**: Verify IDs (e.g., `customer_id=2`, `product_id=1`) and choices (`status="PENDING"`, `payment_type="CASH"`). Copy JSON bodies exactly to avoid parse errors.
- **404 Not Found**: Check resource IDs via GET or `/admin/`.
- **Database Issues**: Reset with `rm db.sqlite3` and `python manage.py migrate`.