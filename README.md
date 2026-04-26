# Gym Membership Management System

A robust, full-stack web application built with Django and Bootstrap 5 designed to help gym administrators efficiently manage clients, memberships, and track payments.

## Features

- **Dashboard Analytics**: View real-time metrics including total clients, active memberships, and recent registrations.
- **Client Management**: Create, Read, Update, and Delete (CRUD) client profiles with contact details.
- **Membership Management**: Assign and track memberships (Monthly, Quarterly, Yearly), monitor start/end dates, and manage payment statuses (Paid/Pending).
- **Search & Filtering**: Quickly find clients by name or phone number, and filter memberships by type or payment status.
- **Secure Access**: The entire application is protected via a secure authentication system requiring admin login.
- **Modern UI**: Clean, responsive frontend powered by Bootstrap 5 and `django-crispy-forms`.

## Tech Stack

- **Backend**: Python, Django (MVT architecture)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Bootstrap Icons
- **Database**: SQLite (Default)

## Setup & Installation

Follow these steps to run the project locally on your machine.

### Prerequisites
- Python 3.8+ installed on your system.

### 1. Navigate to the Project folder
Open your terminal or command prompt in the project's root directory:
```bash
cd "c:\Gym membership management system"
```

### 2. Activate the Virtual Environment
The project relies on an isolated Python virtual environment (`venv`) that includes all the necessary packages.
* On **Windows**:
  ```powershell
  .\venv\Scripts\activate
  ```
* On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3. Database Migrations
Ensure your database is up to date (this step has likely already been completed for you):
```bash
python manage.py migrate
```

### 4. Create an Admin Account
You need a unified admin account to log into the application dashboard.
```bash
python manage.py createsuperuser
```
Follow the prompts to enter your desired username, email, and password.

### 5. Run the Local Server
Start up the built-in Django web server:
```bash
python manage.py runserver
```

### 6. Access the Application
Open any web browser and navigate to:
`http://127.0.0.1:8000/`

Enter the admin credentials you just created to access the full system.

---
*Developed with Django.*
