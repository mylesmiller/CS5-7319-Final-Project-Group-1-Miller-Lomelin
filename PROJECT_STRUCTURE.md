# Project Structure Overview

## Directory Layout

```
CS5-7319-Final-Project-Group-1-Miller-Lomelin/
│
├── README.md                    # Main project documentation
├── PROJECT_STRUCTURE.md         # This file
├── .gitignore                   # Git ignore rules
│
├── Selected/                    # Layered Monolith (MVC) Architecture
│   ├── README.md               # Architecture-specific documentation
│   ├── app.py                  # Application entry point
│   ├── config.py               # Configuration settings
│   ├── models.py               # Database models (Data Layer)
│   ├── routes.py               # Route handlers (Controller Layer)
│   ├── requirements.txt        # Python dependencies
│   │
│   ├── services/               # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── task_service.py     # Task management business logic
│   │   └── notification_service.py  # Notification business logic
│   │
│   ├── templates/              # Jinja2 templates (View Layer)
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── tasks.html
│   │   └── calendar.html
│   │
│   ├── static/                 # Static files
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   │
│   └── tests/                  # Test suite
│       ├── __init__.py
│       ├── test_models.py      # Model tests
│       ├── test_services.py    # Service layer tests
│       └── test_routes.py      # Integration tests
│
└── Unselected/                 # Microservices Architecture
    ├── README.md               # Architecture-specific documentation
    ├── docker-compose.yml      # Docker Compose configuration
    │
    ├── task-service/           # Task Management Service
    │   ├── app.py              # Flask application
    │   ├── config.py           # Service configuration
    │   ├── models.py           # Database models
    │   ├── requirements.txt    # Python dependencies
    │   ├── Dockerfile          # Docker configuration
    │   └── tests/              # Test suite
    │       ├── __init__.py
    │       └── test_task_service.py
    │
    └── notification-service/   # Notification Service
        ├── app.py              # Flask application
        ├── requirements.txt    # Python dependencies
        ├── Dockerfile          # Docker configuration
        └── tests/              # Test suite
            ├── __init__.py
            └── test_notification_service.py
```

## Architecture Comparison

### Layered Monolith (Selected/)
- **Type**: Single deployable application
- **Layers**: Presentation → Business Logic → Data
- **Database**: SQLite (single database)
- **Communication**: Internal function calls
- **Deployment**: Single process
- **Best For**: Small teams, rapid development, simple deployment

### Microservices (Unselected/)
- **Type**: Distributed services
- **Services**: Task Service + Notification Service
- **Database**: SQLite per service (Task Service only)
- **Communication**: HTTP REST APIs
- **Deployment**: Docker containers orchestrated via Docker Compose
- **Best For**: Large teams, independent scaling, fault isolation

## Key Files

### Layered Monolith
- `app.py`: Application factory and entry point
- `models.py`: SQLAlchemy models (User, Task, ActivityLog)
- `routes.py`: Flask route handlers (Controllers)
- `services/task_service.py`: Business logic for tasks
- `services/notification_service.py`: Business logic for notifications

### Microservices
- `task-service/app.py`: REST API for task management
- `task-service/models.py`: Database models for Task Service
- `notification-service/app.py`: REST API for notifications
- `docker-compose.yml`: Orchestrates both services

## Features Implemented

Both architectures implement:
- ✅ Task CRUD operations
- ✅ Task assignment to users
- ✅ Status tracking (pending, in_progress, completed)
- ✅ Priority levels (low, medium, high)
- ✅ Due date management
- ✅ Activity logging
- ✅ Upcoming deadline notifications
- ✅ CSV export
- ✅ Dashboard view
- ✅ Calendar view

## Technology Stack

### Common
- Python 3.11
- Flask 3.0.0
- pytest for testing

### Layered Monolith Specific
- Jinja2 templates
- Flask-SQLAlchemy
- SQLite

### Microservices Specific
- Flask-CORS
- Docker & Docker Compose
- HTTP REST APIs for inter-service communication

## Getting Started

### Layered Monolith
```bash
cd Selected
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Microservices
```bash
cd Unselected
docker compose up --build
```

## Testing

### Layered Monolith
```bash
cd Selected
pytest tests/
```

### Microservices
```bash
# Task Service
cd Unselected/task-service
pytest tests/

# Notification Service
cd Unselected/notification-service
pytest tests/
```

