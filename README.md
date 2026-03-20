# MG Complaint Management System

A web-based complaint management system for MG Motors with automated email notifications.

## Features

- **Admin Authentication**: Secure login with password hashing
- **Complaint Submission Form**: Brand selection, dealership routing, priority levels
- **Automated Email System**: Separate notifications for customers and service teams
- **Database Management**: SQLite with auto-generated complaint IDs (YYYYMMDD-### format)
- **Professional UI**: Responsive design with brand logos
- **Email Integration**: SMTP-based notifications with persistent connections

## Requirements

- Python 3.7+
- Flask
- Gunicorn (for production)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Edit `brand_config.json` to set:
- Email credentials for customer support
- Dealership information
- SMTP server settings

## Running Locally

```bash
PORT=5001 python3 app.py
```

Access at: `http://127.0.0.1:5001/login`

**Default Login:**
- Username: `Admin`
- Password: `Admin@2026`

## Project Structure

```
complaint_system/
├── app.py                 # Main Flask application
├── brand_config.json      # Configuration file
├── requirements.txt       # Dependencies
├── Procfile              # Production configuration
├── templates/            # HTML templates
│   ├── login.html
│   ├── form.html
│   └── success.html
└── static/logos/         # Brand logos
```

## Email System

The system sends two separate emails for each complaint:

1. **Customer Email**: Confirmation message with complaint details
2. **Service Team Email**: Detailed notification with priority level

Each dealership receives notifications for their respective brand complaints.

## Database

Complaints are stored with:
- Auto-generated Complaint ID
- Customer information (name, email, phone)
- Vehicle details (registration number)
- Complaint description and priority
- Timestamp and status

## Deployment

The application is configured for deployment on Render and other cloud platforms using Gunicorn.

## Support

For technical support, refer to the configuration files and inline code documentation.
