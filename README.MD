# 🥩 TamuCuts API

A **Butchery Management System** built with **Django REST Framework (DRF)** as part of the ALX Capstone Project.  
TamuCuts helps streamline butchery operations by managing products, sales, inventory, and employees.

---

##  Features
- Manage meat products (add, update, delete, list)
- Track customer orders and sales
- Manage suppliers and deliveries
- Handle employee records
- User authentication with JWT
- Generate basic reports (future scope)

---
## 📂 Project Structure (planned)
```
TamuCuts-api/
│
├── TamuCuts/ # Main Django project folder (settings, urls, wsgi)
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