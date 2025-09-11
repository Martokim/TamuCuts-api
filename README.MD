# 🥩 TamuCuts API

A **Butchery Management System** built with **Django REST Framework (DRF)** as part of the ALX Capstone Project.  
TamuCuts helps streamline butchery operations by managing products, sales, inventory, and employees.


---
## Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST   | /api/token/ | Authenticate user | No |
| GET/POST | /api/products/ | List/create products | Yes (POST: Admin) |
| GET/POST | /api/orders/ | List/create orders | Yes |
| POST   | /api/stock-transactions/ | Record stock in/out/close | Yes |
| GET    | /api/reports/<date>/ | Daily report (YYYY-MM-DD) | Yes (Admin) |
| GET/POST | /api/scale-readings/ | List/create scale readings | Yes |
| GET/POST | /api/notifications/ | List/create stock notifications | Yes (Admin)
---
## 📂 Project Structure
```
TamuCuts-api/
│
├── tamucuts/              
├── butchery/               
│   ├── migrations/         
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│
├── db.sqlite3              # Development database
├── manage.py               # Django CLI
├── requirements.txt        # Dependencies
├── README.md               # This file
└── .gitignore              # Ignore venv/, __pycache__/, etc.

```

# Setup Instructions 
###  Prerequisites 
- Python 3.8 or higher,  download from [python.org](https://www.python.org/).
- Git (for cloning the repository).
- Optional: Postman or a similar API client for testing endpoints.


### Clone the repo
```
git clone https://github.com/Martokim/TamuCuts-api.git
cd TamuCuts-api
```

### Create and Activate a Virtual Environment
```
python -m venv venv
```
### Install dependancies 
```
pip install -r requirements.txt
```

### Run Database Migrations
```
python manage.py makemigrations
python manage.py migrate
```

### Create a Superuser (Admin Account)
```
python manage.py createsuperuser
```
### Run development server 🚀
```
python manage.py runserver
```

