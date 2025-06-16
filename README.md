# IT Asset Management Portal

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/flask-2.2.x-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

A complete web-based solution for tracking IT assets, their lifecycle, and assignments within an organization.

## Features

- **Asset Management**
  - Add/edit/view IT assets
  - Track purchase details and warranties
  - Manage asset status (Available/Assigned/Maintenance/etc.)
  
- **User Management**
  - Role-based access control (Admin/Manager/User)
  - Department assignment
  - User activity tracking

- **Assignment System**
  - Check-in/check-out assets
  - Transfer between users
  - Due date tracking

- **Reporting**
  - Asset inventory reports
  - Warranty expiration alerts
  - Assignment history
  - Export to Excel

- **Lifecycle Tracking**
  - Complete audit trail
  - Status change history
  - Maintenance records

## Technology Stack

- **Backend**: Python 3.8+, Flask
- **Database**: SQLite (with Flask-SQLAlchemy)
- **Frontend**: Bootstrap 5, Jinja2 templates
- **Key Packages**:
  - Flask-Login for authentication
  - Flask-WTF for forms
  - Pandas for reporting
  - Flask-Migrate for database migrations

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/it-asset-portal.git
   cd it-asset-portal
Project Structure

it_asset_portal/
├── app/
│   ├── __init__.py         # Flask app factory
│   ├── models/             # Database models
│   ├── routes/             # Application routes
│   ├── templates/          # Jinja2 templates
│   ├── static/             # CSS/JS/images
│   ├── forms/              # WTForms classes
│   └── utils/              # Helper functions
├── database/
│   └── it_assets.db        # SQLite database
├── migrations/             # Database migration scripts
├── config.py              # Configuration settings
├── manage.py              # CLI commands
└── run.py                 # Application entry point
   
