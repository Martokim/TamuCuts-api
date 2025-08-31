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
├── TamuCuts/ # Main Django project folder (settings, urls, wsgi
├── products/ # Products app (meat types, stock, pricing)
├── orders/ # Orders app (sales, customer orders)
├── suppliers/ # Suppliers app (meat suppliers, deliveries)
├── employees/ # Employees app (staff records, roles)
│
│
├── requirements.txt    # Python dependencies
├── manage.py           # Django project manager
├── README.md
└── .gitignore          # Ignore venv/, __pycache__/, etc.

```