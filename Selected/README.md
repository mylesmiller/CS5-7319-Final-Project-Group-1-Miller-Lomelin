# Layered Monolith (MVC) Architecture - Task Management System

## Overview

This is a task management system implemented using a Layered Monolith (MVC) architecture. The system provides a simple, unified structure ideal for small development teams, with clear separation of concerns between the presentation, business logic, and data layers.

## Architecture

The application follows a four-layer architecture:

1. **Presentation Layer**: Flask routes and Jinja2 templates (Controllers)
2. **Business Logic Layer**: Service classes in `services/`
3. **Data Access Layer**: Repository pattern in `database/repositories.py`
4. **Data Layer**: SQLAlchemy models and SQLite database

## Features

- Create, edit, and manage tasks
- Assign tasks to team members
- Track progress with status updates
- Dashboard with statistics and notifications
- Calendar view for task deadlines
- In-app notifications for upcoming deadlines
- Activity log of all task updates
- CSV export for reporting

## Technology Stack

- **Python**: 3.11
- **Web Framework**: Flask
- **Templates**: Jinja2
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Testing**: pytest, Flask-Testing
- **Frontend**: HTML/CSS with Vanilla JavaScript

## Setup Instructions

1. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## Running Tests

```bash
pytest tests/
```

## Project Structure

```
Selected/
├── app.py                 # Application entry point
├── config.py             # Configuration settings
├── models.py             # Database models (Data Layer)
├── routes.py             # Route handlers (Presentation/Controller Layer)
├── requirements.txt      # Python dependencies
├── database/             # Data Access Layer (Repository Pattern)
│   └── repositories.py   # Repository classes for data access
├── services/             # Business Logic Layer
│   ├── task_service.py
│   └── notification_service.py
├── templates/            # Jinja2 templates (View Layer)
│   ├── base.html
│   ├── dashboard.html
│   ├── tasks.html
│   └── calendar.html
├── static/               # Static files
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── tests/                # Test files
    ├── test_models.py
    ├── test_services.py
    └── test_routes.py
```

## API Endpoints

- `GET /` - Dashboard
- `GET /tasks` - Task list view
- `GET /calendar` - Calendar view
- `GET /api/tasks` - Get all tasks (JSON)
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/<id>` - Get a specific task
- `PUT /api/tasks/<id>` - Update a task
- `DELETE /api/tasks/<id>` - Delete a task
- `POST /api/tasks/<id>/assign` - Assign a task to a user
- `GET /api/notifications` - Get notifications
- `GET /api/activity` - Get activity log
- `GET /export/csv` - Export tasks to CSV

## Development Notes

- The application uses SQLite for simplicity and easy setup
- All components operate within a single deployable application
- The monolithic design simplifies development and testing
- Source control is managed via GitHub

