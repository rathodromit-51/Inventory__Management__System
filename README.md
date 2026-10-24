# Inventory Management System

A web-based Inventory Management System built with **Python and Django** to help manage products, categories, suppliers, and stock movement from one place. The application includes role-based user accounts and separate dashboards for administrators, managers, and staff.

## Features

- **User accounts:** Registration, login, logout, and profile pages.
- **Role-based access:** Admin, Manager, and Staff roles.
- **Dashboard views:** Role-specific dashboards for monitoring inventory operations.
- **Category management:** Add, view, update, and delete product categories.
- **Product management:** Create, view, update, and delete products, including SKU, category, supplier, quantity, price, reorder level, and description.
- **Supplier management:** Store and maintain supplier contact information.
- **Stock transactions:** Record stock-in and stock-out activity, including quantity, user, notes, and timestamp.
- **Inventory tracking:** Keep product quantities and stock transaction history organized.
- **Django Admin:** Manage application data through Django's built-in administration interface.
- **Responsive templates:** HTML templates with a shared layout and custom CSS.

## Tech Stack

- **Backend:** Python, Django
- **Database:** SQLite (configured by default)
- **Frontend:** HTML, CSS, JavaScript, Django Templates
- **Authentication:** Django authentication with a custom user model

## Project Structure

```text
inventory_management_system/
├── accounts/                 # Custom user model, authentication, roles, dashboards
├── inventory/                # Categories, products, suppliers, stock transactions
├── inventory_management/     # Django project settings and URL configuration
├── static/                   # CSS and JavaScript assets
├── templates/                # Django HTML templates
│   ├── accounts/
│   ├── dashboard/
│   ├── include/
│   └── inventory/
├── manage.py
├── .gitignore
└── README.md
```

## Getting Started

### Prerequisites

- Python installed on your computer
- `pip` (Python package installer)
- Git (optional, for cloning the repository)

### 1. Clone the repository

Replace `YOUR_USERNAME` with your GitHub username and `YOUR_REPOSITORY` with the repository name.

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

If you downloaded the source code as a ZIP file, extract it and open a terminal in the folder containing `manage.py`.

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**

```bat
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Django

The project archive does not include a `requirements.txt` file. Install Django in your active virtual environment. The project's settings were generated for Django 6.1.2, so use a compatible version for your Python installation.

```bash
python -m pip install --upgrade pip
python -m pip install "Django==6.1.2"
```

If that Django version is unavailable for your Python environment, check the project's actual installed version and install a compatible release before proceeding.

### 4. Apply database migrations

The project is configured to use SQLite by default, so no separate database server is required for local development.

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create an administrator account

```bash
python manage.py createsuperuser
```

Follow the prompts to create your account. The project uses a custom user model (`accounts.Profile`), which extends Django's `AbstractUser` and adds role and phone fields.

### 6. Run the development server

```bash
python manage.py runserver
```

Open the application at:

- Main application: http://127.0.0.1:8000/
- Django administration: http://127.0.0.1:8000/admin/

Stop the development server with `Ctrl + C`.

## Main Modules

| Module | Purpose |
|---|---|
| Accounts | User registration, login/logout, profile information, and role-based dashboards |
| Categories | Organize products into categories |
| Products | Maintain product details, SKU, price, quantity, and reorder level |
| Suppliers | Maintain supplier contact details |
| Stock Transactions | Record stock-in and stock-out operations and their history |
| Dashboards | Provide inventory information through role-specific pages |

## Data Models

- **Profile:** Custom user account with role (`Admin`, `Manager`, or `Staff`) and phone number.
- **Category:** Category name and description.
- **Supplier:** Supplier name, email, phone, and creation date.
- **Product:** Product name, unique SKU, category, optional supplier, quantity, price, reorder level, description, and timestamps.
- **StockTransaction:** Product, transaction type (`Stock In` or `Stock Out`), quantity, associated user, note, and timestamp.

## Development Notes

- SQLite is configured in `inventory_management/settings.py` for local development.
- Static assets are stored in `static/`, and page templates are stored in `templates/`.
- The custom user model is configured as `AUTH_USER_MODEL = 'accounts.Profile'`. Keep this setting in place when initializing a new database.
- Ensure role permissions and stock quantity updates are tested before using the application with real inventory data.

## Security Before Deployment

This repository is intended for development and learning. Before deploying it publicly:

1. Move `SECRET_KEY` into an environment variable and replace any exposed development key.
2. Set `DEBUG = False` and configure `ALLOWED_HOSTS` for your deployment.
3. Keep database files, passwords, API keys, and other secrets out of Git.
4. Use HTTPS and review Django's deployment checklist.
5. Test authentication, role permissions, input validation, and stock transaction behavior.

## Future Improvements

- Search, filtering, and pagination for inventory records
- Low-stock alerts based on each product's reorder level
- Reports and charts for stock movement and inventory value
- Export inventory reports to CSV or Excel
- Automated tests for inventory operations and role permissions
- Production-ready environment-variable and deployment configuration

## Contributing

Contributions and suggestions are welcome. Fork the repository, create a feature branch, make your changes, and submit a pull request.

## License

No license has been specified yet. Add a `LICENSE` file before distributing or reusing this project under an open-source license.
