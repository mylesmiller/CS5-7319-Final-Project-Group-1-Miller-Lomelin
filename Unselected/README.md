# Microservices Architecture - Task Management System

## Overview

This is a task management system implemented using a Microservices architecture. The system is split into four independent services that communicate via HTTP APIs:

1. **Frontend Service**: Provides the web interface (HTML/CSS/JS) and proxies requests to backend services
2. **User Service**: Manages all user-related operations (user CRUD, authentication data)
3. **Task Service**: Manages all core task management functions (CRUD, assignments, status transitions, activity log)
4. **Notification Service**: Handles sending alerts and reminders for events like task assignments or upcoming deadlines

## Architecture

The microservices architecture provides:
- **Independent Services**: Each service can be developed, deployed, and scaled independently
- **Fault Isolation**: If one service fails, the other continues to operate
- **Service Communication**: Services communicate via REST APIs
- **Containerization**: Each service runs in its own Docker container

## Services

### Frontend Service (Port 5003)

Provides the web interface for the microservices system:
- Dashboard with statistics and notifications
- Task management interface
- Calendar view
- CSV export functionality
- Proxies API requests to backend services

**Endpoints:**
- `GET /` - Dashboard
- `GET /tasks` - Task list view
- `GET /calendar` - Calendar view
- `GET /export/csv` - Export tasks to CSV
- `GET /health` - Health check
- All API endpoints proxy to respective backend services

### User Service (Port 5002)

Manages all user-related operations:
- Create, read, update, delete users
- User validation and lookup
- User information management

**Endpoints:**
- `GET /health` - Health check
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get a specific user
- `POST /api/users` - Create a new user
- `PUT /api/users/<id>` - Update a user
- `DELETE /api/users/<id>` - Delete a user
- `GET /api/users/by-username/<username>` - Get user by username
- `GET /api/users/by-email/<email>` - Get user by email
- `POST /api/users/validate` - Validate multiple user IDs

### Task Service (Port 5000)

Manages all task-related operations:
- Create, read, update, delete tasks
- Assign tasks to users (validates with User Service)
- Track task status and priority
- Maintain activity logs
- Query upcoming deadlines
- Proxies user requests to User Service

**Endpoints:**
- `GET /health` - Health check
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/<id>` - Get a specific task
- `PUT /api/tasks/<id>` - Update a task
- `DELETE /api/tasks/<id>` - Delete a task
- `POST /api/tasks/<id>/assign` - Assign a task
- `GET /api/tasks/upcoming` - Get upcoming tasks
- `GET /api/activity` - Get activity log
- `GET /api/users` - Get all users (proxies to User Service)
- `GET /api/users/<id>` - Get a user (proxies to User Service)

### Notification Service (Port 5001)

Handles all notification operations:
- Receives events from Task Service
- Sends notifications for task assignments
- Checks for upcoming deadlines
- Supports email notifications (configurable)

**Endpoints:**
- `GET /health` - Health check
- `POST /api/events` - Handle events from other services
- `GET /api/notifications` - Get all notifications
- `POST /api/notifications/upcoming-deadlines` - Check upcoming deadlines
- `POST /api/notifications/clear` - Clear notifications (testing)

## Technology Stack

- **Python**: 3.11
- **Web Framework**: Flask
- **Database**: SQLite (Task Service)
- **Containerization**: Docker, Docker Compose
- **Testing**: pytest, httpx
- **Communication**: HTTP REST APIs

## Setup Instructions

### Using Docker Compose (Recommended)

1. **Navigate to the Unselected directory**:
   ```bash
   cd Unselected
   ```

2. **Build and start services**:
   ```bash
   docker compose up --build
   ```
   
   **Note**: If you get "command not found", try `docker-compose` (with hyphen) for older Docker versions, or update to Docker Desktop which includes `docker compose` (with space).

3. **Access the web interface**:
   - **Frontend (Web UI)**: http://localhost:5003
   - Dashboard: http://localhost:5003/
   - Tasks: http://localhost:5003/tasks
   - Calendar: http://localhost:5003/calendar
   
   **API Endpoints** (for direct API access):
   - User Service API: `http://localhost:5002/health` (health check)
   - Task Service API: `http://localhost:5000/health` (health check)
   - Notification Service API: `http://localhost:5001/health` (health check)
   - Frontend Service: `http://localhost:5003/health` (health check)

### Manual Setup

#### User Service

1. **Navigate to user-service directory**:
   ```bash
   cd user-service
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the service**:
   ```bash
   python app.py
   ```

#### Task Service

1. **Navigate to task-service directory**:
   ```bash
   cd task-service
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**:
   ```bash
   export NOTIFICATION_SERVICE_URL=http://localhost:5001
   export USER_SERVICE_URL=http://localhost:5002
   ```

5. **Run the service**:
   ```bash
   python app.py
   ```

#### Notification Service

1. **Navigate to notification-service directory**:
   ```bash
   cd notification-service
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the service**:
   ```bash
   python app.py
   ```

## Running Tests

### User Service Tests
```bash
cd user-service
pytest tests/
```

### Task Service Tests
```bash
cd task-service
pytest tests/
```

### Notification Service Tests
```bash
cd notification-service
pytest tests/
```

## Service Communication

### Task Service ↔ User Service
The Task Service communicates with the User Service to:
- Validate user IDs when creating or assigning tasks
- Fetch user information (username, email) for notifications
- Proxy user-related API requests

### Task Service → Notification Service
The Task Service communicates with the Notification Service by sending HTTP POST requests to `/api/events` when certain events occur:

- **task_created**: When a new task is created
- **task_assigned**: When a task is assigned to a user (includes user email from User Service)
- **task_status_changed**: When a task's status changes

The Notification Service processes these events and generates appropriate notifications.

## Configuration

### Environment Variables

**User Service:**
- `DATABASE_URL`: Database connection string (default: `sqlite:///user_service.db`)
- `SECRET_KEY`: Secret key for the application

**Task Service:**
- `DATABASE_URL`: Database connection string (default: `sqlite:///task_service.db`)
- `NOTIFICATION_SERVICE_URL`: URL of the notification service (default: `http://notification-service:5001`)
- `USER_SERVICE_URL`: URL of the user service (default: `http://user-service:5002`)
- `SECRET_KEY`: Secret key for the application

**Notification Service:**
- `SECRET_KEY`: Secret key for the application
- `SMTP_ENABLED`: Enable email notifications (default: `false`)
- `SMTP_SERVER`: SMTP server address
- `SMTP_PORT`: SMTP server port
- `SMTP_USER`: SMTP username
- `SMTP_PASSWORD`: SMTP password

## Project Structure

```
Unselected/
├── frontend-service/
│   ├── app.py              # Frontend Service application
│   ├── requirements.txt    # Dependencies
│   ├── Dockerfile          # Docker configuration
│   ├── templates/          # Jinja2 templates
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── tasks.html
│   │   └── calendar.html
│   └── static/             # Static files
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
├── user-service/
│   ├── app.py              # User Service application
│   ├── models.py           # Database models
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Dependencies
│   ├── Dockerfile          # Docker configuration
│   └── tests/              # Test files
├── task-service/
│   ├── app.py              # Task Service application
│   ├── models.py           # Database models (no User model)
│   ├── config.py           # Configuration
│   ├── requirements.txt    # Dependencies
│   ├── Dockerfile          # Docker configuration
│   └── tests/              # Test files
├── notification-service/
│   ├── app.py              # Notification Service application
│   ├── requirements.txt    # Dependencies
│   ├── Dockerfile          # Docker configuration
│   └── tests/              # Test files
└── docker-compose.yml      # Docker Compose configuration
```

## Development Notes

- Services communicate synchronously via HTTP for simplicity
- In production, consider using a message queue (RabbitMQ, Kafka) for async communication
- Each service has its own database:
  - User Service: SQLite for user data
  - Task Service: SQLite for tasks and activity logs (stores user IDs only, not user data)
  - Notification Service: Stateless, stores notifications in memory (consider a database for production)
- Task Service validates user IDs with User Service before creating/assigning tasks
- Docker Compose orchestrates all three services and creates a shared network
- Health check endpoints are provided for service monitoring
- Service dependencies: Task Service depends on User Service

## Advantages of Microservices Architecture

1. **Scalability**: Each service can be scaled independently based on demand
2. **Fault Isolation**: Failure in one service doesn't bring down the entire system
3. **Technology Flexibility**: Each service can use different technologies if needed
4. **Team Autonomy**: Different teams can work on different services
5. **Deployment Independence**: Services can be deployed separately
6. **Modularity**: Separation of User Service allows for better user management and potential authentication/authorization features
7. **Single Responsibility**: Each service has a clear, focused responsibility

## Disadvantages

1. **Complexity**: More complex than monolithic architecture
2. **Network Latency**: Inter-service communication adds latency
3. **Data Consistency**: Maintaining consistency across services is challenging
4. **Deployment Overhead**: More services to deploy and manage
5. **Testing Complexity**: Integration testing is more complex

